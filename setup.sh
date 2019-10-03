#!/bin/bash
set -x

# Create and use python virtual environment
cd api
virtualenv -p python3 python-venv
python-venv/bin/pip install -r requirements.txt
python-venv/bin/flask db upgrade
cd ..

# Create and use node virtual environment
#api/python-venv/bin/python -m nodeenv node-venv
#source node-venv/bin/activate
#npm install --global @vue/cli @vue/cli-init

# Install packages from bubblecheck-vue/packages.json
#cd bubblecheck-vue
#npm install
#cd - 
