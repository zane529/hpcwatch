# -*- coding: utf-8 -*-
import os
from influxdb import InfluxDBClient
import awsUtil


HOST = awsUtil.get_aws_parameter('InfluxdbPrivateIp')
PORT = 8086
USER = awsUtil.get_aws_parameter('InfluxdbUser')
PASS = awsUtil.get_aws_parameter('InfluxdbPass')
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
