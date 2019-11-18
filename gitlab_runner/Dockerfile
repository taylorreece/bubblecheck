FROM python:3.6-alpine

RUN apk update && apk upgrade
RUN apk add bash git nodejs npm openssh
RUN npm install -g serverless
RUN pip install awscli
