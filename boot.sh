#!/bin/bash
source venv/bin/activate
exec gunicorn -b :8000 -w 2 --access-logfile - --error-logfile - app:app
