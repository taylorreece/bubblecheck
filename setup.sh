#!/bin/bash
set -x

# Create and use python virtual environment
virtualenv -p python3 python-venv
source python-venv/bin/activate
pip install -r requirements.txt

# Create and use node virtual environment
nodeenv node-venv
source node-venv/bin/activate
npm install -g vue-cli
