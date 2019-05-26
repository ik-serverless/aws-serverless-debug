#!/usr/bin/env python

import json
import boto3
import os
# List sedrets
region = os.environ['REGION']
secretsname = os.environ['SECRETS_NAME']

secclient = boto3.client('secretsmanager')
'''
require Action
{
    "Sid": "NotSupportResourceLevelPermissions",
    "Effect": "Allow",
    "Action": [
        "secretsmanager:ListSecrets",
        "secretsmanager:ListSecretVersionIds"
    ],
    "Resource": [
        "*"
    ]
}
'''
def list():
    response = client.list_secrets()
    for secret in response['SecretList']:
        print(secret['Name'])


'''
Get secret Value
require Action
{
    "Sid": "NotSupportResourceLevelPermissions",
    "Effect": "Allow",
    "Action": [
        "secretsmanager:GetSecretValue"
    ],
    "Resource": [
        "arn:aws:secretsmanager:<region>:<accountid>:secret:<secretname>-*"
    ]
}
'''
def get_secret(secret):
    response = secclient.get_secret_value(
        SecretId=secret
    )
    print(response['SecretString'])


# list()
get_secret(secretsname)
