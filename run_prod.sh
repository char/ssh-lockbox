#!/usr/bin/env bash

gunicorn "$@" -w ${WORKERS:-4} -k uvicorn.workers.UvicornWorker --log-level warning lockbox:app
