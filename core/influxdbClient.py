# -*- coding: utf-8 -*-
import os
from influxdb import InfluxDBClient
import awsUtil

HOST = awsUtil.get_aws_parameter('dbhost')
PORT = awsUtil.get_aws_parameter('dbport')
USER = awsUtil.get_aws_parameter('dbuser')
PASS = awsUtil.get_aws_parameter('dbpass')

DBNAME = 'hpccollect'


def get_influxdb_client():
    """
    Get influxdb client.
    :return:
    """
    client = None
    try:
        client = InfluxDBClient(HOST, PORT, USER, PASS, DBNAME)
    except Exception as e:
        print('Get InfluxDB client error !!!')
        print(e)
    return client
