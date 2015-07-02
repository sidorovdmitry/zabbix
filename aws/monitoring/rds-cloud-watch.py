#!/usr/bin/env python

# Author: Dmitry Sidorov
# Requires boto3 lib: https://boto3.readthedocs.org/en/latest/guide/quickstart.html

# Set access and secret keys to ~/.aws/credentials 
# Set region of RDS to ~/.aws/config
# Run python rds-cloud-watch.py rds-instance-name metric:
# python rds-cloud-watch.py testinstance CPUUtilization

import sys
import boto3
from datetime import *
import math

instance = sys.argv[1]
metric = sys.argv[2]

mlist = {
    'CPUUtilization': 'Percent',
    'FreeStorageSpace': 'Bytes',
    'FreeableMemory': 'Bytes',
    'ReadIOPS': 'Count/Second',
    'WriteIOPS': 'Count/Second',
    'DatabaseConnections': 'Count'
}

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
hour = datetime.today().hour
minute =  datetime.today().minute

client = boto3.client('cloudwatch')
answer = client.get_metric_statistics(
    Namespace = 'AWS/RDS',
    MetricName = metric,
    Dimensions=[
        {
            'Name': 'DBInstanceIdentifier',
            'Value': instance
        },
    ],
    StartTime=datetime(year, month, day, 10, 10-1),
    EndTime=datetime(year, month, day, 10, 10),
    Period = 60,
    Statistics=['Maximum'],
    Unit=mlist[metric]
)
value = answer.get('Datapoints')[0].get('Maximum')
print int(round(value))
