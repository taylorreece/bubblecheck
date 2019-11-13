#!/usr/bin/env bash
set -euxo pipefail

ENVIRONMENT=$1

cd api/
STACK_NAME=$(serverless info --stage ${ENVIRONMENT} | grep '^stack: [a-z-]*$' | sed 's/stack: //')
REACT_S3_BUCKET=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[0].Outputs[?OutputKey=='ReactS3BucketName'].OutputValue" --output text)
cd ../web
npm run-script build
aws s3 sync build/ s3://${REACT_S3_BUCKET}/