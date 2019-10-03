#!/bin/bash
set -xe

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/../api
source python-venv/bin/activate
flask db upgrade
cd -
cd $DIR
PYTHONPATH=$DIR/../api/
./test_api.py

cd $CWD
