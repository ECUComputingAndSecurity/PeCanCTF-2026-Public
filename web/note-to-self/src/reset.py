import os
import time
import datetime

import bcrypt
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
INTERVAL   = int(os.environ.get("RESET_INTERVAL", 300))

ADMIN_NOTES = [
    {
        "title":   "Maintenance window",
        "content": "Scheduled downtime Sunday 02:00–04:00 UTC.\nRemember to snapshot Redis before taking the service down.",
        "color":   "#b3d9ff",
    },
    {
        "title":   "TODO",
        "content": "- Add rate limiting to /login\n- Review user list and remove inactive accounts\n- Set up log forwarding",
        "color":   "#ffd700",
    },
    {
        "title":   "New dev onboarding",
        "content": "Shared the staging creds with the new dev. Need to rotate after their first week — they've been using the shared account.",
        "color":   "#ffb3ba",
    },
    {
        "title":   "Reminder",
        "content": "Ask the team to stop putting sensitive stuff in their notes. This is a shared service.",
        "color":   "#a8e6cf",
    },
]


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def seed_admin(r):
    admin_password = os.urandom(16).hex()
    pw_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    r.hset("user:admin", mapping={"password_hash": pw_hash, "role": "admin", "created_at": _now()})
    r.sadd("users", "admin")
    for note in ADMIN_NOTES:
        note_id = os.urandom(8).hex()
        r.hset(f"note:{note_id}", mapping={
            "username":   "admin",
            "title":      note["title"],
            "content":    note["content"],
            "color":      note["color"],
            "created_at": _now(),
        })
        r.set(f"note:{note_id}:body", note["content"])
        r.rpush("notes:admin", note_id)


def seed_internal_config(r):
    r.hset("config:internal", mapping={
        "environment":  "production",
        "debug":        "false",
        "last_updated": _now(),
    })


def reset(r):
    r.flushdb()
    seed_admin(r)
    seed_internal_config(r)
    print(f"[{_now()}] Reset complete", flush=True)


def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    for _ in range(20):
        try:
            r.ping()
            break
        except redis.ConnectionError:
            time.sleep(0.5)
    else:
        raise RuntimeError("Could not connect to Redis")

    print(f"[{_now()}] Resetter started — interval {INTERVAL}s", flush=True)
    reset(r)
    while True:
        time.sleep(INTERVAL)
        reset(r)


if __name__ == "__main__":
    main()
