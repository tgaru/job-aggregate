#!/bin/sh

apt install tmux > /dev/null 2>&1 &&
pip3 install -r requirements.txt > /dev/null 2>&1 &&
tmux new -d -s job_aggregator 'python3 start.py'