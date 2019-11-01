import boto3

class DynamoDB(object):
    def init_app(self, app):
        self.dynamo_endpoint = app.config['DYNAMO_ENDPOINT']
        self.dynamo_table = app.config['DYNAMO_TABLE']
        self.aws_region = app.config['AWS_REGION']
        self.client = boto3.client('dynamodb',
            endpoint_url=self.dynamo_endpoint,
            region_name=self.aws_region
        )
        self.table = boto3.resource('dynamodb', 
            endpoint_url=self.dynamo_endpoint,
            region_name=self.aws_region).Table(self.dynamo_table)

dynamodb = DynamoDB()