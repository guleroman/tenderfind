#!/bin/bash

cd app
su -m root -c "gunicorn --log-level info --log-file=gunicorn.log -k gevent -w 2 --name app -b 0.0.0.0:8888 --reload app:app"