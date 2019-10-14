#!/usr/bin/env python3

import argparse
import boto3
import re
import time

session = boto3.Session(profile_name='bubblecheck')
cf = session.client('cloudformation')
route53 = session.client('route53')
cognito = session.client('cognito-idp')

def create_stack(args):
    with open(args.file, 'r') as template_file:
        template_body = template_file.read()
    stack_response = cf.create_stack(
        StackName=args.stack_name,
        TemplateBody=template_body,
        Parameters=[
            {
                'ParameterKey': 'DomainName',
                'ParameterValue': args.url
            },
            {
                'ParameterKey': 'UserPoolName',
                'ParameterValue': args.userpool_name
            }
        ],
        EnableTerminationProtection=True)
    stack_status = cf.describe_stacks(StackName=args.stack_name)['Stacks'][0]
    events = cf.describe_stack_events(StackName=args.stack_name)
    seen_events = list()
    while 'COMPLETE' not in stack_status['StackStatus']:
        for event in [e for e in events['StackEvents'] if e['EventId'] not in seen_events]:
            if event['LogicalResourceId'] == 'AuthTlsCertificate' and 'ResourceStatusReason' in event.keys():
                resource_status_reason = event['ResourceStatusReason']
                regex = re.compile('Content of DNS Record is: {Name: (.*),Type: (.*),Value: (.*)}')
                if regex.match(resource_status_reason):
                    record_source, record_type, record_dest = regex.match(resource_status_reason).groups()
                    print("Creating temporary record '{}' -{}-> '{}'".format(record_source, record_type, record_dest))
                    route53.change_resource_record_sets(
                        HostedZoneId='Z2CLTAGI77SNE8', # bubblecheck.app
                        ChangeBatch={
                            'Comment': 'Record set for verifying certificate manager domain ownership.',
                            'Changes': [
                                {
                                    'Action': 'UPSERT',
                                    'ResourceRecordSet': {
                                        'Name': record_source,
                                        'Type': record_type,
                                        'TTL': 300,
                                        'ResourceRecords': [{'Value': record_dest}]
                                    }
                                }
                            ]
                        }
                    )
            print('{}\t{}'.format(event['LogicalResourceId'], event['EventId']))
            seen_events.append(event['EventId'])
        time.sleep(10)
        stack_status = cf.describe_stacks(StackName=args.stack_name)['Stacks'][0]
        events = cf.describe_stack_events(StackName=args.stack_name)
    stack_status = cf.describe_stacks(StackName=args.stack_name)['Stacks'][0]
    if stack_status['StackStatus'] != 'CREATE_COMPLETE':
        print("An error occurred spinning up the stack")
        exit(1)
    domain_response = cognito.describe_user_pool_domain(Domain=args.url)
    print("Creating temporary record '{}' -Alias-> '{}'".format(args.url, domain_response['DomainDescription']['CloudFrontDistribution']))
    route53.change_resource_record_sets(
        HostedZoneId='Z2CLTAGI77SNE8', # bubblecheck.app
        ChangeBatch={
            'Comment': 'Record set for cognito auth endpoint',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': args.url,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': 'Z2FDTNDATAQYW2', # cloudfront zone id
                            'DNSName': domain_response['DomainDescription']['CloudFrontDistribution'],
                            'EvaluateTargetHealth': False
                        }
                    }
                }
            ]
        }
    )
    print("Success!")

def update_stack(args):
    with open(args.file, 'r') as template_file:
        template_body = template_file.read()
    stack_response = cf.update_stack(
        StackName=args.stack_name,
        TemplateBody=template_body,
        Parameters=[
            {
                'ParameterKey': 'DomainName',
                'ParameterValue': args.url
            },
            {
                'ParameterKey': 'UserPoolName',
                'ParameterValue': args.userpool_name
            },
        ])

def parse_args():
    parent_parser = argparse.ArgumentParser(description='Create or update a Cognito stack.', add_help=False)
    parent_parser.add_argument('--file', default='cognito.yaml', help='Name of YAML file to apply')
    parent_parser.add_argument('--url', default='auth.bubblecheck.app', help='URL users will hit for auth')
    parent_parser.add_argument('--stack-name', default='cognito-auth')
    parent_parser.add_argument('--userpool-name', default='bubblecheck-auth')

    parser = argparse.ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers()

    create_subparser = subparsers.add_parser('create', help='Create a new cognito stack', parents=[parent_parser])
    create_subparser.set_defaults(func=create_stack)
    update_subparser = subparsers.add_parser('update', help='Update an existing cognito stack', parents=[parent_parser])
    update_subparser.set_defaults(func=update_stack)

    args = parser.parse_args()
    if 'func' not in dir(args):
        parser.print_help()
        exit()
    return args

if __name__ == '__main__':
    args = parse_args()
    args.func(args)