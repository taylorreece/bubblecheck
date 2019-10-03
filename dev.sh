#!/bin/bash
./run-node.sh &
cd api
python-venv/bin/python ./app.py
