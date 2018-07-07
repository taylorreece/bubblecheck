#!/bin/bash

CWD=$pwd
DIR=$(dirname $0)
cd $DIR/..
source node-venv/bin/activate
npm install bubblecheck-vue
cd bubblecheck-vue
npm run build

cd $CWD