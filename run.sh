#!/bin/bash

# webui
python /app/web/app.py  > /var/log/app-webui.log 2>&1 &
# crontab
crontab  > /var/log/app-crontab.log 2>&1 &

# just keep this script running
while [[ true ]]; do
    sleep 1
done
