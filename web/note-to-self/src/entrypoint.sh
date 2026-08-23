#!/bin/sh
redis-server --daemonize yes
python reset.py &
sleep 3
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
