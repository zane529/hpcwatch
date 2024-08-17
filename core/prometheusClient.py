# -*- coding: utf-8 -*-
from prometheus_client import push_to_gateway
from prometheus_client.exposition import basic_auth_handler
import awsUtil
import os


cluster_name = os.getenv('CLUSTER_NAME')

if cluster_name:
    HOST = awsUtil.get_aws_parameter(cluster_name + '_dbhost')
    PORT = awsUtil.get_aws_parameter(cluster_name + '_dbport')
    USER = awsUtil.get_aws_parameter(cluster_name + '_dbuser')
    PASS = awsUtil.get_aws_parameter(cluster_name + '_dbpass')
else:
    HOST = awsUtil.get_aws_parameter('dbhost')
    PORT = awsUtil.get_aws_parameter('dbport')
    USER = awsUtil.get_aws_parameter('dbuser')
    PASS = awsUtil.get_aws_parameter('dbpass')

def auth_handler(url, method, timeout, headers, data):
    return basic_auth_handler(url, method, timeout, headers, data, USER, PASS)


def push_info(job, registry, client):
    """
    Get PushGateway client.
    :return:
    """
    
    try:
        print("Metrics being pushed to Pushgateway:")
        for metric in registry.collect():
            print(f"Metric Name: {metric.name}")
            print(f"Metric Help: {metric.documentation}")
            for sample in metric.samples:
                print(f"  Sample: {sample.name}, Value: {sample.value}, Labels: {sample.labels}")
            print("---")

        push_to_gateway('%s:%s' %(HOST, PORT), job=job, registry=registry, grouping_key={"client":client}, handler=auth_handler)
    except Exception as e:
        print('Push message error !!!')
        print(e)

