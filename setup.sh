#!/bin/bash
set -x

# Environment file for docker-compose
PWD_FULL_PATH=$(readlink .)
if [[ "$PWD_FULL_PATH" = "" ]];
then
  PWD_FULL_PATH=$PWD
fi
echo "PWD_FULL_PATH=$PWD_FULL_PATH" > .env

# Doing this for now... I'll have better auth env variable mechanisms later
echo "COGNITO_URL=auth.bubblecheck.app" >> .env
echo "COGNITO_CLIENT_ID=3e2h6ltcienr4l0nc1h4l6fl6o" >> .env
