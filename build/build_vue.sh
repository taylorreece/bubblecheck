#!/bin/bash
set -ex 

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/..
source node-venv/bin/activate
npm install bubblecheck-vue
cd bubblecheck-vue
npm install --global @vue/cli @vue/cli-init
npm run build

cd $CWD