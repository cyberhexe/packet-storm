#!/bin/bash

service nginx start

bash inotify.sh &
python3 packet-storm-cli.py -ed docs/Cybersecurity
