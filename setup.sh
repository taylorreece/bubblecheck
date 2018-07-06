#!/bin/bash
set -x

# Create and use python virtual environment
virtualenv -p python3 python-venv
python-venv/bin/pip install -r requirements.txt

# Create and use node virtual environment
python-venv/bin/python -m nodeenv node-venv
source node-venv/bin/activate
npm install -g vue-cli
