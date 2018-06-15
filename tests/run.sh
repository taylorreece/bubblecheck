#!/bin/bash

CWD=$pwd
DIR=$(dirname $0)
cd $DIR
source ../venv/bin/activate
./test_api.py

cd $CWD