#!/usr/bin/env bash

# location: /usr/local/bin/internet_timer.sh

cd /home/pi/git/internet_timer
python3 internet_timer.py >> /tmp/internet_timer.log 2>&1
