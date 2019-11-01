FROM python:3-alpine

RUN pip install awscli
RUN apk update && apk add bash

COPY ./seed_dynamo.sh /seed_dynamo.sh 
COPY json/ /json/

CMD sleep 3 && bash /seed_dynamo.sh ${DYNAMO_TABLE} ${DYNAMO_ENDPOINT}
