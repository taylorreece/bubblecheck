#!/bin/bash
set -xe

CWD=$pwd
DIR=$(dirname $0)
cd $DIR
cd ..
FLASK_APP=bubblecheck flask db upgrade || true
cd $DIR
./test_api.py

cd $CWD