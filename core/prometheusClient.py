# -*- coding: utf-8 -*-
from prometheus_client import push_to_gateway
from prometheus_client.exposition import basic_auth_handler
import awsUtil

HOST = awsUtil.get_aws_parameter('dbhost')
PORT = awsUtil.get_aws_parameter('dbport')
USER = awsUtil.get_aws_parameter('dbuser')
PASS = awsUtil.get_aws_parameter('dbpass')

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

