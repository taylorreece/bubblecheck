#!/bin/bash
set -x

# Create and use python virtual environment
virtualenv -p python3 python-venv
python-venv/bin/pip install -r requirements.txt

# Create and use node virtual environment
python-venv/bin/python -m nodeenv node-venv
source node-venv/bin/activate
npm install --global @vue/cli @vue/cli-init

# Install packages from bubblecheck-vue/packages.json
npm install bubblecheck-vue