#!/bin/bash
set -xe

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/..
source python-venv/bin/activate
FLASK_APP=bubblecheck flask db upgrade
cd $DIR
./test_api.py

cd $CWD
