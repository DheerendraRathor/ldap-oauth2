#!/bin/bash
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/

PORT_DEV=
ROOT=
KILL=

source $ABSOLUTE_PATH/settings.sh

PORT=$PORT_DEV
KILL=$KILL

cd $ROOT

# Kill network process on port $PORT
fuser -k $PORT/tcp

# Exit after killing by fuser if KILL is true
if [ "$KILL" = true ] ; then
    exit 1
fi

gunicorn iitbapp.wsgi \
    --bind=0.0.0.0:$PORT \
     -c gunicorn_conf.py \
    --log-level=info \
    --reload \
    --log-file "logs/gunicorn_logs.log" &
