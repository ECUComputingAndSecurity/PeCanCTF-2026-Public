import os
import hashlib
import datetime
import functools
from typing import cast

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, g
import jwt
import bcrypt
import redis
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
FLAG       = os.environ.get("FLAG", "pecan{f4k3_fl4g}")


def get_redis():
    r = getattr(g, "_redis", None)
    if r is None:
        r = g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return r


@app.teardown_appcontext
def close_redis(_):
    r = getattr(g, "_redis", None)
    if r is not None:
        r.close()



def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


# --- JWT helpers ---

def make_jwt(username, role):
    now         = datetime.datetime.now(datetime.timezone.utc)
    jwt_secret  = os.urandom(32).hex()
    redis_key   = "jwt_secrets:" + hashlib.sha256(jwt_secret.encode()).hexdigest()
    expiry_time = datetime.timedelta(hours=24)

    r = get_redis()
    r.set(redis_key, jwt_secret, ex=int(expiry_time.total_seconds()))

    iv      = os.urandom(16)
    padder  = PKCS7(128).padder()
    padded  = padder.update(FLAG.encode()) + padder.finalize()
    enc     = Cipher(algorithms.AES(bytes.fromhex(jwt_secret)), modes.CBC(iv)).encryptor()
    ct      = enc.update(padded) + enc.finalize()
    encrypted_flag = (iv + ct).hex()

    return jwt.encode(
        {"sub": username, "role": role, "iat": now, "exp": now + expiry_time, "data": encrypted_flag},
        jwt_secret,
        algorithm="HS256",
        headers={"kid": redis_key},
    )


def decode_jwt(token):
    try:
        header = jwt.get_unverified_header(token)
        if not "kid" in header:
            return None
        
        r = get_redis()
        jwt_secret = cast(str, r.get(header['kid']))
        
        return jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except Exception:
        return None


# --- Auth decorators ---

def require_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("login_page"))
        payload = decode_jwt(token)
        if not payload:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Invalid token"}), 401
            return redirect(url_for("login_page"))
        g.user = payload
        return f(*args, **kwargs)
    return wrapper


def require_admin(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect(url_for("login_page"))
        payload = decode_jwt(token)
        if not payload or payload.get("role") != "admin":
            return render_template("403.html"), 403
        g.user = payload
        return f(*args, **kwargs)
    return wrapper


# --- Page routes ---

@app.route("/")
def index():
    token = request.cookies.get("token")
    if token and decode_jwt(token):
        return redirect(url_for("notes_page"))
    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").encode()
    r = get_redis()
    user = cast(dict, r.hgetall(f"user:{username}"))
    if not user or not bcrypt.checkpw(password, user["password_hash"].encode()):
        return render_template("login.html", error="Invalid username or password")
    token = make_jwt(username, user["role"])
    resp = make_response(redirect(url_for("notes_page")))
    resp.set_cookie("token", token, httponly=True, samesite="Lax", max_age=86400)
    return resp


@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if not username or not password:
        return render_template("signup.html", error="All fields are required")
    if len(username) < 3 or len(username) > 32:
        return render_template("signup.html", error="Username must be 3-32 characters")
    if len(password) < 6:
        return render_template("signup.html", error="Password must be at least 6 characters")
    if username.lower() == "admin":
        return render_template("signup.html", error="That username is not available")
    r = get_redis()
    if r.exists(f"user:{username}"):
        return render_template("signup.html", error="Username already taken")
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    r.hset(f"user:{username}", mapping={
        "password_hash": pw_hash,
        "role":          "user",
        "created_at":    _now(),
    })
    r.sadd("users", username)
    note_id = os.urandom(8).hex()
    welcome = f"Welcome to StickyNotes, {username}! Create your first note below."
    r.hset(f"note:{note_id}", mapping={
        "username":   username,
        "title":      "Welcome!",
        "content":    welcome,
        "color":      "#a8e6cf",
        "created_at": _now(),
    })
    r.set(f"note:{note_id}:body", welcome)
    r.lpush(f"notes:{username}", note_id)
    token = make_jwt(username, "user")
    resp = make_response(redirect(url_for("notes_page")))
    resp.set_cookie("token", token, httponly=True, samesite="Lax", max_age=86400)
    return resp


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login_page")))
    resp.delete_cookie("token")
    return resp


@app.route("/notes")
@require_auth
def notes_page():
    return render_template("notes.html", username=g.user["sub"], role=g.user.get("role", "user"))


@app.route("/admin")
@require_admin
def admin_page():
    r = get_redis()
    usernames = sorted(cast(set, r.smembers("users")))
    users = []
    user_notes = {}
    for uname in usernames:
        u = cast(dict, r.hgetall(f"user:{uname}"))
        users.append({
            "username":   uname,
            "role":       u.get("role", "user"),
            "created_at": u.get("created_at", ""),
        })
        note_ids = cast(list, r.lrange(f"notes:{uname}", 0, -1))
        notes = []
        for nid in note_ids:
            n = cast(dict, r.hgetall(f"note:{nid}"))
            if n:
                notes.append({"id": nid, **n})
        user_notes[uname] = notes
    return render_template(
        "admin.html",
        users=users,
        user_notes=user_notes,
        username=g.user["sub"],
        role="admin",
    )


_ALLOWED_COMMANDS = {
    "get", "keys", "scan", "type", "ttl", "pttl", "exists",
    "hgetall", "hget", "hkeys", "hvals", "hlen",
    "lrange", "llen",
    "smembers", "scard",
}

@app.route("/api/admin/diagnostics", methods=["POST"])
@require_admin
def api_admin_diagnostics():
    data    = request.get_json(silent=True) or {}
    command = str(data.get("command") or "").strip().lower()
    args    = [str(a) for a in (data.get("args") or [])]
    if not command:
        return jsonify({"error": "No command provided"}), 400
    if command not in _ALLOWED_COMMANDS:
        return jsonify({"error": "Command not permitted"}), 403
    r = get_redis()
    try:
        result = r.execute_command(command, *args)
        if isinstance(result, tuple):
            result = list(result)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/admin/users/<username>", methods=["DELETE"])
@require_admin
def api_delete_user(username):
    r = get_redis()
    if not r.exists(f"user:{username}"):
        return jsonify({"error": "User not found"}), 404
    if r.hget(f"user:{username}", "role") == "admin":
        return jsonify({"error": "Cannot delete the admin account"}), 403
    note_ids = cast(list, r.lrange(f"notes:{username}", 0, -1))
    for nid in note_ids:
        r.delete(f"note:{nid}", f"note:{nid}:body")
    r.delete(f"notes:{username}")
    r.delete(f"user:{username}")
    r.srem("users", username)
    return jsonify({"ok": True})


# --- API routes ---

@app.route("/api/notes", methods=["GET"])
@require_auth
def api_get_notes():
    r = get_redis()
    username = g.user["sub"]
    note_ids = cast(list, r.lrange(f"notes:{username}", 0, -1))
    notes = []
    for nid in note_ids:
        n = cast(dict, r.hgetall(f"note:{nid}"))
        if n:
            notes.append({"id": nid, **n})
    return jsonify(notes)


@app.route("/api/notes", methods=["POST"])
@require_auth
def api_create_note():
    data     = request.get_json(silent=True) or {}
    title    = str(data.get("title")   or "").strip()[:100]
    content  = str(data.get("content") or "").strip()[:2000]
    color    = data.get("color", "#ffd700")
    allowed_colors = {"#ffd700", "#a8e6cf", "#ffb3ba", "#b3d9ff", "#e8b4ff"}
    if color not in allowed_colors:
        color = "#ffd700"
    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400
    username = g.user["sub"]
    r = get_redis()
    note_id = os.urandom(8).hex()
    r.hset(f"note:{note_id}", mapping={
        "username":   username,
        "title":      title,
        "content":    content,
        "color":      color,
        "created_at": _now(),
    })

    r.set(f"note:{note_id}:body", content)
    r.lpush(f"notes:{username}", note_id)
    return jsonify({"id": note_id, "title": title, "content": content, "color": color}), 201


@app.route("/api/notes/<note_id>", methods=["DELETE"])
@require_auth
def api_delete_note(note_id):
    username = g.user["sub"]
    r = get_redis()
    owner = r.hget(f"note:{note_id}", "username")
    if owner is None:
        return jsonify({"error": "Note not found"}), 404
    if owner != username:
        return jsonify({"error": "Note not found"}), 404
    r.delete(f"note:{note_id}", f"note:{note_id}:body")
    r.lrem(f"notes:{username}", 0, note_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
