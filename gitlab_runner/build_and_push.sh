#!/bin/bash

docker build . -t taylorreece/bc-build-server
docker push taylorreece/bc-build-server:latest