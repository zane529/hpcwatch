# -*- coding: utf-8 -*-
from prometheus_client import push_to_gateway
from prometheus_client.exposition import basic_auth_handler
import awsUtil

# HOST = awsUtil.get_aws_parameter('InfluxdbPrivateIp')
# PORT = 9091
# USER = awsUtil.get_aws_parameter('InfluxdbUser')
# PASS = awsUtil.get_aws_parameter('InfluxdbPass')

HOST = '10.0.0.132'
PORT = 9091
USER = 'admin'
PASS = 'du@15a7pxdEGVyC'

def auth_handler(url, method, timeout, headers, data):
    return basic_auth_handler(url, method, timeout, headers, data, USER, PASS)


def push_info(job, registry):
    """
    Get influxdb client.
    :return:
    """
    
    try:
        push_to_gateway('%s:%s' %(HOST, PORT), job=job, registry=registry, handler=auth_handler)
    except Exception as e:
        print('Push message error !!!')
        print(e)

