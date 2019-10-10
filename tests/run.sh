#!/bin/bash
set -xe

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/../api
source ../python-venv/bin/activate
flask db upgrade
cd -
cd $DIR
PYTHONPATH=$DIR/../api/
# Disabling for now until we get better tests
#./test_api.py

cd $CWD
