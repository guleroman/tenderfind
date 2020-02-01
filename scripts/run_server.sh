#!/bin/bash

cd app
su -m root -c "gunicorn --log-level info --log-file=gunicorn.log -k gevent -w 3 --name app -b 0.0.0.0:7777 --reload app:app --preload --timeout 90"