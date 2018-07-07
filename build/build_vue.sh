#!/bin/bash
set -ex 

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/..
source node-venv/bin/activate
cd bubblecheck-vue
npm install
npm install --global @vue/cli @vue/cli-init
npm run build

cd $CWD