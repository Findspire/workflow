#!/usr/bin/env bash

# Run as vagrant, not root
if [[ "$USER" != "vagrant" ]]; then
    exec sudo -u vagrant "$0"
fi

# Fail as soon as any command fails
set -e

# Start a detached tmux session
tmux -2 new-session -d

# Setup windows for the Django server and a Celery worker
tmux new-window -n 'Django' ./runserver
tmux new-window -n 'Celery' ./runworker

# Select the Django window
tmux select-window -t:1
