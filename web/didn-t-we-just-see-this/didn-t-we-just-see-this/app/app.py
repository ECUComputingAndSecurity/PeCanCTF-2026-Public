import os
import secrets
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from pathlib import Path

import requests
from flask import (
    Flask,
    Response,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    stream_with_context,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


DATABASE = os.environ.get("DATABASE_PATH", "/data/devhub.db")
BOT_URL = os.environ.get("BOT_URL", "http://127.0.0.1:5001").rstrip("/")
FLAG = os.environ["FLAG"]
SUPPORT_COOLDOWN_SECONDS = int(os.environ.get("SUPPORT_COOLDOWN_SECONDS", "10"))
SUPPORT_EXECUTOR = None
SUPPORT_EXECUTOR_PID = None
SUPPORT_EXECUTOR_LOCK = threading.Lock()


def get_support_executor():
    global SUPPORT_EXECUTOR, SUPPORT_EXECUTOR_PID
    current_pid = os.getpid()
    with SUPPORT_EXECUTOR_LOCK:
        if SUPPORT_EXECUTOR is None or SUPPORT_EXECUTOR_PID != current_pid:
            SUPPORT_EXECUTOR = ThreadPoolExecutor(
                max_workers=8,
                thread_name_prefix="support",
            )
            SUPPORT_EXECUTOR_PID = current_pid
    return SUPPORT_EXECUTOR


def connect_db():
    db = sqlite3.connect(DATABASE, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA busy_timeout = 10000")
    return db


def init_db():
    Path(DATABASE).parent.mkdir(parents=True, exist_ok=True)
    db = connect_db()
    db.execute("PRAGMA journal_mode = WAL")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Developer',
            challenge_id TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            body TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'message',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(recipient_id) REFERENCES users(id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS support_requests (
            user_id INTEGER PRIMARY KEY,
            last_requested_at REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS runtime_secrets (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    generated_secrets = {
        "bot_token": secrets.token_urlsafe(48),
        "support_password": secrets.token_urlsafe(32),
        "flask_secret": secrets.token_hex(32),
    }
    db.executemany(
        """
        INSERT OR IGNORE INTO runtime_secrets (name, value)
        VALUES (?, ?)
        """,
        generated_secrets.items(),
    )
    db.commit()
    runtime_secrets = {
        row["name"]: row["value"]
        for row in db.execute("SELECT name, value FROM runtime_secrets")
    }
    db.close()
    return runtime_secrets


def load_runtime_secrets():
    db = connect_db()
    try:
        return {
            row["name"]: row["value"]
            for row in db.execute("SELECT name, value FROM runtime_secrets")
        }
    finally:
        db.close()


if os.environ.get("DEVHUB_DB_INITIALIZED") == "1":
    RUNTIME_SECRETS = load_runtime_secrets()
else:
    RUNTIME_SECRETS = init_db()
SUPPORT_PASSWORD = RUNTIME_SECRETS["support_password"]

app = Flask(__name__)
app.config.update(
    SECRET_KEY=RUNTIME_SECRETS["flask_secret"],
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "false").lower()
    == "true",
)


def get_db():
    if "db" not in g:
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def runtime_secret_direct(name):
    db = connect_db()
    try:
        row = db.execute(
            "SELECT value FROM runtime_secrets WHERE name = ?",
            (name,),
        ).fetchone()
    finally:
        db.close()
    if row is None:
        raise RuntimeError(f"Missing runtime secret: {name}")
    return row["value"]


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@app.before_request
def load_user():
    g.user = current_user()


@app.context_processor
def inbox_status():
    if g.user is None:
        return {"unread_inbox_count": 0}
    row = get_db().execute(
        """
        SELECT COUNT(*) AS unread_count
        FROM messages
        WHERE recipient_id = ?
          AND category = 'support'
          AND read_at IS NULL
        """,
        (g.user["id"],),
    ).fetchone()
    return {"unread_inbox_count": row["unread_count"]}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def require_challenge(view):
    @wraps(view)
    @login_required
    def wrapped(challenge_id, *args, **kwargs):
        if g.user["challenge_id"] != challenge_id:
            flash("That page is not part of your DevHub workspace.")
            return redirect(url_for("challenge_home", challenge_id=g.user["challenge_id"]))
        return view(challenge_id, *args, **kwargs)

    return wrapped


def csrf_token():
    token = session.get("csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def validate_csrf():
    return request.form.get("csrf_token") == session.get("csrf_token")


def generate_challenge_id():
    db = get_db()
    while True:
        challenge_id = secrets.token_hex(8)
        existing = db.execute(
            "SELECT 1 FROM users WHERE challenge_id = ? LIMIT 1", (challenge_id,)
        ).fetchone()
        if not existing:
            return challenge_id


def support_username(challenge_id):
    return f"support_{challenge_id}"


def support_for_challenge(challenge_id):
    return get_db().execute(
        """
        SELECT * FROM users
        WHERE challenge_id = ? AND role = 'Support'
        """,
        (challenge_id,),
    ).fetchone()


def check_support_rate_limit(user_id):
    now = time.time()
    cutoff = now - SUPPORT_COOLDOWN_SECONDS
    cursor = get_db().execute(
        """
        INSERT INTO support_requests (user_id, last_requested_at)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            last_requested_at = excluded.last_requested_at
        WHERE support_requests.last_requested_at <= ?
        """,
        (user_id, now, cutoff),
    )
    get_db().commit()
    if cursor.rowcount == 0:
        row = get_db().execute(
            "SELECT last_requested_at FROM support_requests WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        wait = int(SUPPORT_COOLDOWN_SECONDS - (now - row["last_requested_at"])) + 1
        return False, max(wait, 1)
    return True, 0


app.jinja_env.globals["csrf_token"] = csrf_token


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.")
        elif username.startswith("support_"):
            flash("That username is reserved.")
        elif not username.replace("_", "").isalnum():
            flash("Use only letters, numbers, and underscores.")
        else:
            challenge_id = generate_challenge_id()
            try:
                cursor = get_db().execute(
                    """
                    INSERT INTO users (username, password_hash, role, challenge_id)
                    VALUES (?, ?, 'Developer', ?)
                    """,
                    (
                        username,
                        generate_password_hash(password),
                        challenge_id,
                    ),
                )
                get_db().execute(
                    """
                    INSERT INTO users (username, password_hash, role, challenge_id)
                    VALUES (?, ?, 'Support', ?)
                    """,
                    (
                        support_username(challenge_id),
                        generate_password_hash(SUPPORT_PASSWORD),
                        challenge_id,
                    ),
                )
                get_db().commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                csrf_token()
                return redirect(url_for("challenge_home", challenge_id=challenge_id))
            except sqlite3.IntegrityError:
                get_db().rollback()
                flash("That username is already taken.")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            csrf_token()
            return redirect(url_for("challenge_home", challenge_id=user["challenge_id"]))
        flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/c/<challenge_id>")
@app.route("/c/<challenge_id>/")
@app.route("/c/<challenge_id>/<path:extra>")
@require_challenge
def challenge_home(challenge_id, extra=None):
    support = support_for_challenge(challenge_id)
    return render_template(
        "challenge.html",
        challenge_id=challenge_id,
        support_username=(
            support["username"] if support else support_username(challenge_id)
        ),
    )


@app.route("/c/<challenge_id>/settings")
@app.route("/c/<challenge_id>/settings/")
@app.route("/c/<challenge_id>/settings/<path:extra>")
@require_challenge
def settings(challenge_id, extra=None):
    api_key = FLAG if g.user["role"] == "Support" else f"dev_live_{challenge_id[:12]}"
    return render_template(
        "settings.html",
        user=g.user,
        extra=extra,
        api_key=api_key,
        challenge_id=challenge_id,
    )


def create_support_reply_direct(challenge_id, recipient_id, body):
    db = connect_db()
    try:
        support = db.execute(
            """
            SELECT * FROM users
            WHERE challenge_id = ? AND role = 'Support'
            """,
            (challenge_id,),
        ).fetchone()
        if support is None:
            return False
        db.execute(
            """
            INSERT INTO messages (sender_id, recipient_id, body, category)
            VALUES (?, ?, ?, 'support')
            """,
            (support["id"], recipient_id, body),
        )
        db.commit()
        return True
    finally:
        db.close()


def process_support_ticket(challenge_id, user_id, message, portal_host):
    time.sleep(1)
    try:
        response = requests.post(
            f"{BOT_URL}/ticket",
            json={
                "challenge_id": challenge_id,
                "message": message,
                "portal_host": portal_host,
            },
            headers={
                "Authorization": f"Bearer {runtime_secret_direct('bot_token')}"
            },
            timeout=5,
        )
        if response.status_code == 202:
            job_id = response.json()["job_id"]
            deadline = time.monotonic() + 120
            while time.monotonic() < deadline:
                result = requests.get(
                    f"{BOT_URL}/ticket/{job_id}",
                    headers={
                        "Authorization": (
                            f"Bearer {runtime_secret_direct('bot_token')}"
                        )
                    },
                    timeout=5,
                )
                if result.status_code == 200:
                    reply = result.json().get(
                        "reply",
                        "Thanks for contacting DevHub Support.",
                    )
                    break
                if result.status_code != 202:
                    result.raise_for_status()
                time.sleep(0.5)
            else:
                raise requests.Timeout("Support ticket processing timed out")
        else:
            response.raise_for_status()
            reply = response.json().get(
                "reply",
                "Thanks for contacting DevHub Support.",
            )
    except requests.RequestException:
        reply = "DevHub Support is temporarily unavailable. Please try again in a moment."
    create_support_reply_direct(challenge_id, user_id, reply)


@app.route("/c/<challenge_id>/support", methods=["GET", "POST"])
@app.route("/c/<challenge_id>/support/", methods=["GET", "POST"])
@app.route("/c/<challenge_id>/support/<path:extra>", methods=["GET", "POST"])
@require_challenge
def support(challenge_id, extra=None):
    if request.method == "POST":
        if not validate_csrf():
            flash("Invalid form token.")
            return redirect(url_for("support", challenge_id=challenge_id))
        message = request.form.get("message", "").strip()
        if not message:
            flash("Tell DevHub Support what you need help with.")
            return redirect(url_for("support", challenge_id=challenge_id))
        if support_for_challenge(challenge_id) is None:
            flash("DevHub Support is temporarily unavailable.")
            return redirect(url_for("support", challenge_id=challenge_id))
        allowed, wait = check_support_rate_limit(g.user["id"])
        if not allowed:
            flash(f"Please wait {wait} seconds before opening another support ticket.")
            return render_template("support.html", challenge_id=challenge_id)
        get_support_executor().submit(
            process_support_ticket,
            challenge_id,
            g.user["id"],
            message,
            request.host,
        )
        flash("Your support ticket was submitted. Watch your inbox for a reply.")
    return render_template("support.html", challenge_id=challenge_id)


@app.route("/c/<challenge_id>/inbox")
@app.route("/c/<challenge_id>/inbox/")
@app.route("/c/<challenge_id>/inbox/<path:extra>")
@app.route("/c/<challenge_id>/messages")
@app.route("/c/<challenge_id>/messages/")
@app.route("/c/<challenge_id>/messages/<path:extra>")
@require_challenge
def inbox(challenge_id, extra=None):
    rows = get_db().execute(
        """
        SELECT messages.id, messages.body, messages.created_at, messages.category, users.username AS sender
        FROM messages
        JOIN users ON users.id = messages.sender_id
        WHERE messages.recipient_id = ?
        ORDER BY messages.created_at DESC
        """,
        (g.user["id"],),
    ).fetchall()
    get_db().execute(
        """
        UPDATE messages
        SET read_at = CURRENT_TIMESTAMP
        WHERE recipient_id = ?
          AND category = 'support'
          AND read_at IS NULL
        """,
        (g.user["id"],),
    )
    get_db().commit()
    return render_template("messages.html", messages=rows, challenge_id=challenge_id)


@app.route("/c/<challenge_id>/events")
@require_challenge
def events(challenge_id):
    user_id = g.user["id"]
    last_event_id = request.headers.get("Last-Event-ID")
    if last_event_id and last_event_id.isdigit():
        last_id = int(last_event_id)
    else:
        row = get_db().execute(
            """
            SELECT COALESCE(MAX(id), 0) AS latest_id
            FROM messages
            WHERE recipient_id = ? AND category = 'support'
            """,
            (user_id,),
        ).fetchone()
        last_id = row["latest_id"]

    @stream_with_context
    def stream():
        nonlocal last_id
        while True:
            db = connect_db()
            rows = db.execute(
                """
                SELECT id
                FROM messages
                WHERE recipient_id = ? AND category = 'support' AND id > ?
                ORDER BY id ASC
                """,
                (user_id, last_id),
            ).fetchall()
            db.close()
            for row in rows:
                last_id = row["id"]
                yield f"id: {last_id}\nevent: inbox\ndata: New support reply received\n\n"
            yield ": keepalive\n\n"
            time.sleep(2)

    return Response(
        stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/healthz")
def healthz():
    return "ok"
