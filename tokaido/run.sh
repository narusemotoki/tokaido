#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
uwsgi --http=:8080 --ini-paste-logged ${SCRIPT_DIR}/wsgi.ini
