#!/bin/bash
set -xe

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/..
source python-venv/bin/activate
cd $DIR/../api
flask db upgrade
cd -
cd $DIR
PYTHONPATH=$DIR/../api/
./test_api.py

cd $CWD
