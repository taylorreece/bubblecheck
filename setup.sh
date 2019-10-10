#!/bin/bash
set -x

# Create and use python virtual environment
virtualenv -p python3 python-venv
cd api
../python-venv/bin/pip install -r requirements.txt
../python-venv/bin/flask db upgrade
cd ..

# Environment file for docker-compose
PWD_FULL_PATH=$(readlink .)
if [[ "$PWD_FULL_PATH" = "" ]];
then
  PWD_FULL_PATH=$PWD
fi
echo "PWD_FULL_PATH=$PWD_FULL_PATH" > .env

# Create and use node virtual environment
#api/python-venv/bin/python -m nodeenv node-venv
#source node-venv/bin/activate
#npm install --global @vue/cli @vue/cli-init

# Install packages from bubblecheck-vue/packages.json
#cd bubblecheck-vue
#npm install
#cd - 
