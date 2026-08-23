#!/bin/sh
set -eu

cd /srv/app
python -c "import app"
export DEVHUB_DB_INITIALIZED=1

exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/devhub.conf
