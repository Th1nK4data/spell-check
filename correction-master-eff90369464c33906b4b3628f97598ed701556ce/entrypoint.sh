#!/bin/bash

# - bind on 8000 port
# - sapwn 2 worker process
#   will be restarted automatically.

gunicorn --bind 0.0.0.0:$CR_DOCKER_PORT --timeout=0 --workers=2 --log-config log_config --log-level debug --capture-output server:api
