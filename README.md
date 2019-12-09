# bubblecheck
[![CICD Pipeline](https://gitlab.com/taylorreece/bubblecheck/badges/master/pipeline.svg)](https://gitlab.com/taylorreece/bubblecheck/pipelines)
[![Code Coverage](https://gitlab.com/taylorreece/bubblecheck/badges/master/coverage.svg?job=coverage)](https://gitlab.com/taylorreece/bubblecheck)

This repo contains all the code we'll need for the BubbleCheck rewrite.

* api/ contains a flask-based API that web and mobile clients connect to
* api/ also contains serverless.js code required to deploy a dev or production environment to AWS, complete with API gateway, S3 bucket for static React files, and a deployment of the flask app into Lambda
* docker/ contains several docker images for local development
* gitlab_runner/ contains a docker image used by gitlab-ci for deployments
* web/ contains a ReactJS front-end for bubblecheck

To run a local instance of bubblecheck, with local directories mapped to your local docker images (for instantenous recompiling and fast dev'ing):

  * Run `$ ./setup.sh` to set up some docker environment variables
  * Run `docker-compose up`

A continuous integration / deployment stack is available at https://dev.bubblecheck.app
