#!/bin/bash

DYNAMO_TABLE=$1
DYNAMO_ENDPOINT=$2

aws dynamodb create-table \
    --table-name ${DYNAMO_TABLE} \
    --endpoint-url ${DYNAMO_ENDPOINT} \
    --attribute-definitions \
        AttributeName=key1,AttributeType=S AttributeName=key2,AttributeType=S \
    --key-schema AttributeName=key1,KeyType=HASH AttributeName=key2,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 \
    --global-secondary-indexes IndexName=SecondaryGSI,\
KeySchema=["{AttributeName=key2,KeyType=HASH}","{AttributeName=key1,KeyType=RANGE}"],\
Projection="{ProjectionType=ALL}",\
ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"

echo "Create dummy user"
aws dynamodb put-item \
    --table-name ${DYNAMO_TABLE} \
    --endpoint-url ${DYNAMO_ENDPOINT} \
    --item file://json/user.json

echo "Attach them to a course"
aws dynamodb put-item \
    --table-name ${DYNAMO_TABLE} \
    --endpoint-url ${DYNAMO_ENDPOINT} \
    --item file://json/course.json

echo "Create four sections for the course"
for i in {1..4}
do
    aws dynamodb put-item \
        --table-name ${DYNAMO_TABLE} \
        --endpoint-url ${DYNAMO_ENDPOINT} \
        --item "{\
\"key1\":{\"S\":\"section_000$i\"},\
\"key2\":{\"S\":\"course_0000\"},\
\"section_name\":{\"S\":\"Hour $i\"}}"
    echo "Creating student exams to be associated with the exam and sections"

    for j in {1..2}
    do
        aws dynamodb put-item \
        --table-name ${DYNAMO_TABLE} \
        --endpoint-url ${DYNAMO_ENDPOINT} \
        --item "{
\"key1\": {\"S\": \"exam_0000\"},
\"key2\": {\"S\": \"studentexam_00$i$j\"},
\"section\": {\"S\": \"section_000$i\"},
\"answers\": {\"S\": \"ABCCDEDCB\"}
}"
    done
done

echo "Creating an exam"
aws dynamodb put-item \
    --table-name ${DYNAMO_TABLE} \
    --endpoint-url ${DYNAMO_ENDPOINT} \
    --item file://json/exam.json
