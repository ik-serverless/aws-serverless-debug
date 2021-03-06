import json
import sys
import os
import boto3
import base64
import socket
from urllib import request
from pathlib import Path

from botocore.exceptions import ClientError

region = os.environ['REGION']
secretsname = os.environ['SECRETS_NAME']
secclient = boto3.client('secretsmanager')


def lambda_handler(event, context):
    print("Lambda Debug Network")
    # resolver configuration file
    read_file('files.cfg')
    secrets_manager_get(secretsname)
    hosts('hosts.cfg')
    url_resolves('request.cfg')
    # dns_show_entries()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def port_is_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(ip,port)
    if result == 0:
        print f'port {port} for ip {ip} is open'
    else:
        print f'port {port} for ip {ip} is NOT open'
    sock.close()

def read_file(filepath):
    # Make it generic. If file not found, just error it
    print("\n\tReading file: {}\n".format(filepath))
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            fileline = line.strip()
            print("\n\t\tReading file: '{}'\n".format(fileline))
            my_file=Path(line.strip())
            if my_file.exists():
                with open(fileline) as ff:
                    for cnti, linei in enumerate(ff):
                        print("\t\t{}".format(linei))
    print("\n")


def secrets_manager_list():
    print("Retrieving all secret names")
    response = secclient.list_secrets()
    for secret in response['SecretList']:
        print(secret['Name'])


def secrets_manager_get(secret):
    print("Retrieving secret: {}".format(secret))
    response = secclient.get_secret_value(
        SecretId=secret
    )
    print(response['SecretString'])


def hosts(filepath):
    print("Resolving hosts from file config: {}".format(filepath))
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            hostname = line.strip()
            print("host '{}'\n".format(hostname))
            hostname_resolves(hostname=hostname)


def hostname_resolves(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print("Host {} resolved {}\n".format(hostname, ip))
    except Exception as e:
        print("Host {} not resolved. Error {}\n".format(hostname, e))

def url_resolves(filepath):
    print("Trying to request url data from file: {}".format(filepath))
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            value = line.strip()
            print("url '{}'\n".format(value))
            url_request(value)

def url_request(url):
    try:
        contents = request.urlopen("https://secretsmanager.us-west-2.amazonaws.com").read()
        print("URL {} response {}\n".format(url, contents))
    except Exception as e:
        print("Url {} not accessible. Error {}\n".format(url, e))

def dns_show_entries():
    import dns.resolver
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ['8.8.8.8']
    answer = my_resolver.query('google.com')
    for data in answer:
        print(data)
