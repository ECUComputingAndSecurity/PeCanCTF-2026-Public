import hmac
import os
import queue
import random
import re
import sqlite3
import threading
import time
import uuid
from dataclasses import dataclass, field
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request


BASE_URL = os.environ.get("CHALLENGE_BASE_URL", "http://127.0.0.1").rstrip("/")
VISIT_DELAY_SECONDS = int(os.environ.get("VISIT_DELAY_SECONDS", "2"))
DATABASE = os.environ.get("DATABASE_PATH", "/data/devhub.db")
BOT_WORKERS = 4

app = Flask(__name__)


VALID_REPLIES = [
    "Thanks! I was able to open the page you provided and have forwarded it to engineering.",
    "I checked the DevHub page in your ticket and passed it to the team for investigation.",
    "The page loaded successfully on my side. I've attached it to an engineering review.",
    "Your report has been escalated. Someone from engineering will take a look shortly.",
    "The page looked normal when I opened it, but I've asked engineering to double-check.",
    "The page opened successfully. Recently viewed pages can sometimes take a moment to reflect changes.",
]

SCRIPTLIKE_REPLIES = [
    "Please send the issue as plain text. I can't process scripts or embedded content in support tickets.",
    "I noticed content that looks like markup or script, so I did not open any links from that ticket.",
    "For safety reasons, support tickets with script-like content are reviewed as plain text only.",
    "I couldn't process that ticket as a page report. Please include a plain DevHub page link instead.",
]

NO_LINK_REPLIES = [
    "Could you include the DevHub page where the issue occurs?",
    "I couldn't find a page reference in your report. A page URL helps us reproduce the issue.",
    "To investigate a UI issue, please include the relevant DevHub page.",
    "Thanks for contacting DevHub Support. If this is about a portal page, include the DevHub URL in the issue description.",
]

EXTERNAL_REPLIES = [
    "For security reasons I can only access pages hosted inside DevHub.",
    "That link appears to be outside DevHub, so I wasn't able to open it.",
    "Support reviews are limited to DevHub-hosted pages.",
    "I can only open links inside this DevHub portal, so I did not open the outside link in your ticket.",
]

INVALID_REPLIES = [
    "I couldn't identify a valid DevHub page in your request.",
    "The page reference in your ticket doesn't look like a DevHub portal URL.",
    "I wasn't able to determine which DevHub page should be reviewed.",
    "I couldn't identify a valid DevHub portal page in your request.",
]

UNAVAILABLE_REPLIES = [
    "Engineering is currently busy. Please try again shortly.",
    "The review queue is temporarily unavailable.",
    "We're experiencing a larger-than-usual support backlog right now.",
    "DevHub Support is temporarily unavailable. Please try again in a moment.",
]


@dataclass
class TicketJob:
    job_id: str
    challenge_id: str
    path: str
    status: str = "queued"
    reply: str | None = None
    created_at: float = field(default_factory=time.time)


JOB_QUEUE = queue.Queue()
JOBS = {}
JOBS_LOCK = threading.Lock()


def log(message):
    print(message, flush=True)


def choose_reply(pool):
    return random.choice(pool)


def connect_db_readonly():
    database_uri = f"file:{DATABASE}?mode=ro"
    db = sqlite3.connect(database_uri, uri=True, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout = 10000")
    return db


def read_runtime_secret(name):
    with connect_db_readonly() as db:
        row = db.execute(
            "SELECT value FROM runtime_secrets WHERE name = ?",
            (name,),
        ).fetchone()
    if row is None:
        raise RuntimeError(f"Missing runtime secret: {name}")
    return row["value"]


def authorized():
    expected = f"Bearer {read_runtime_secret('bot_token')}"
    received = request.headers.get("Authorization", "")
    return hmac.compare_digest(received, expected)


def wait_for_app(session):
    for _ in range(60):
        try:
            response = session.get(f"{BASE_URL}/healthz", timeout=2)
            if response.ok:
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Challenge app did not become ready")


def login(session, username, password):
    response = session.post(
        f"{BASE_URL}/login",
        data={"username": username, "password": password},
        timeout=5,
        allow_redirects=True,
    )
    response.raise_for_status()
    if "/login" in response.url:
        raise RuntimeError("Support login failed")


def support_username(challenge_id):
    return f"support_{challenge_id}"


def visit_as_support(path, username, password):
    with requests.Session() as session:
        wait_for_app(session)
        login(session, username, password)
        response = session.get(f"{BASE_URL}{path}", timeout=5)
        response.raise_for_status()
        time.sleep(VISIT_DELAY_SECONDS)


def candidate_links(message):
    candidates = re.findall(r"https?://[^\s<>'\"]+|/[^\s<>'\"]+", message or "")
    return [candidate.rstrip(".,);]") for candidate in candidates]


def contains_scriptlike_content(message):
    indicators = (
        r"<\s*/?\s*[a-z][a-z0-9-]*(?:\s|>|/)",
        r"<\s*script",
        r"<\s*img",
        r"<\s*svg",
        r"<\s*iframe",
        r"onerror\s*=",
        r"onload\s*=",
        r"javascript:",
        r"document\.cookie",
        r"fetch\s*\(",
        r"eval\s*\(",
    )
    return any(
        re.search(indicator, message or "", re.IGNORECASE)
        for indicator in indicators
    )


def normalize_host(value):
    value = (value or "").strip().lower()
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else f"http://{value}")
    return parsed.netloc


def classify_link(candidate, challenge_id, portal_host):
    parsed = urlparse(candidate)
    challenge_prefix = f"/c/{challenge_id}"
    allowed_host = normalize_host(portal_host)

    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return "invalid", None

    if parsed.scheme in ("http", "https"):
        if not allowed_host or normalize_host(parsed.netloc) != allowed_host:
            return "external", None
        path = parsed.path
    elif candidate.startswith("/"):
        if candidate.startswith("//"):
            return "external", None
        path = parsed.path
    else:
        return "invalid", None

    if path == f"{challenge_prefix}/events" or path.startswith(
        f"{challenge_prefix}/events/"
    ):
        return "invalid", None

    if path == challenge_prefix or path.startswith(f"{challenge_prefix}/"):
        if parsed.query:
            path = f"{path}?{parsed.query}"
        return "valid", path
    return "invalid", None


def parse_ticket_link(message, challenge_id, portal_host):
    if contains_scriptlike_content(message):
        return "scriptlike", None
    candidates = candidate_links(message)
    if not candidates:
        return "none", None
    saw_external = False
    for candidate in candidates:
        kind, path = classify_link(candidate, challenge_id, portal_host)
        if kind == "valid":
            return "valid", path
        if kind == "external":
            saw_external = True
    if saw_external:
        return "external", None
    return "invalid", None


def process_job(job):
    try:
        with JOBS_LOCK:
            job.status = "running"
        visit_as_support(
            job.path,
            support_username(job.challenge_id),
            read_runtime_secret("support_password"),
        )
        log(f"Visited support ticket path: {job.path}")
        reply = choose_reply(VALID_REPLIES)
    except Exception as error:
        log(f"Support ticket {job.job_id} failed: {error}")
        reply = choose_reply(UNAVAILABLE_REPLIES)
    finally:
        with JOBS_LOCK:
            job.reply = reply
            job.status = "done"
        JOB_QUEUE.task_done()


def ticket_worker():
    while True:
        process_job(JOB_QUEUE.get())


for worker_number in range(BOT_WORKERS):
    threading.Thread(
        target=ticket_worker,
        name=f"ticket-worker-{worker_number + 1}",
        daemon=True,
    ).start()


@app.post("/ticket")
def ticket():
    if not authorized():
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    challenge_id = data.get("challenge_id", "")
    message = data.get("message", "")
    portal_host = data.get("portal_host", "")
    if not challenge_id:
        return jsonify({"error": "missing challenge_id"}), 400

    kind, path = parse_ticket_link(message, challenge_id, portal_host)
    if kind == "scriptlike":
        return jsonify({"ok": True, "reply": choose_reply(SCRIPTLIKE_REPLIES)})
    if kind == "none":
        return jsonify({"ok": True, "reply": choose_reply(NO_LINK_REPLIES)})
    if kind == "external":
        return jsonify({"ok": True, "reply": choose_reply(EXTERNAL_REPLIES)})
    if kind == "invalid":
        return jsonify({"ok": True, "reply": choose_reply(INVALID_REPLIES)})

    job = TicketJob(
        job_id=uuid.uuid4().hex,
        challenge_id=challenge_id,
        path=path,
    )
    with JOBS_LOCK:
        JOBS[job.job_id] = job
    JOB_QUEUE.put(job)
    return jsonify({"ok": True, "job_id": job.job_id}), 202


@app.get("/ticket/<job_id>")
def ticket_result(job_id):
    if not authorized():
        return jsonify({"error": "unauthorized"}), 401
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            return jsonify({"error": "ticket not found"}), 404
        if job.status != "done":
            return jsonify({"ok": True, "status": job.status}), 202
        JOBS.pop(job_id, None)
        return jsonify(
            {
                "ok": True,
                "status": "done",
                "reply": job.reply,
                "visited_path": job.path,
            }
        )


@app.get("/healthz")
def healthz():
    return "ok"
