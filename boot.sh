#!/bin/bash
exec gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b :8000