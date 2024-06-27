# -*- coding: utf-8 -*-
import os
from tokenize import Name
import urllib3
import psutil
import json
from processinfo import ProcInfo
import boto3
import requests

def get_aws_parameter(key):
    """
    Get aws parameter.
    """
    result = None
    try:
        ssm_client = boto3.client('ssm')
        response = ssm_client.get_parameter(Name = key)
        result = response['Parameter']['Value']
    except Exception as e:
        print(e)
    return result

def get_instance_metadata():
    """
    Get instance metadata.
    :return: json format metadata.
    {
    "devpayProductCodes": null,
    "availabilityZone": "us-west-2a",
    "instanceId": "i-0346506d3d1960e8c",
    "pendingTime": "2024-06-26T10:22:37Z",
    "marketplaceProductCodes": null,
    "region": "us-west-2",
    "imageId": "ami-051cb319371f89591",
    "version": "2017-09-30",
    "architecture": "x86_64",
    "billingProducts": null,
    "kernelId": null,
    "ramdiskId": null,
    "privateIp": "10.0.17.68",
    "instanceType": "c6i.large",
    "accountId": "763309664766"
    }
    """
    TOKEN_URL = "http://169.254.169.254/latest/api/token"
    headers = {'X-aws-ec2-metadata-token-ttl-seconds': '21600'}
    response = requests.put(TOKEN_URL, headers=headers)
    token = response.text

    METADATA_URL = "http://169.254.169.254/latest/dynamic/instance-identity/document"
    headers = {'X-aws-ec2-metadata-token': token}
    response = requests.get(METADATA_URL, headers=headers)
    metadata = response.json()
    return json.dumps(metadata, indent=4)

def get_aws_instance_type():
    """
    Get aws instance type.
    """
    result = None
    url = 'http://169.254.169.254/latest/meta-data/instance-type'
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url)
        if r and r.data:
            result = r.data.decode('utf-8')
    except Exception as e:
        print('Get instance id error!!!')
        print(e)
    return result

def get_aws_instance_id():
    """
    Get aws instance id.
    :return:
    """
    result = None
    url = 'http://169.254.169.254/latest/meta-data/instance-id'
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url)
        if r and r.data:
            result = r.data.decode('utf-8')
    except Exception as e:
        print('Get instance id error!!!')
        print(e)
    return result


def getFileSize(filePath, size=0):
    """
    Get the folder size.
    """
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size


def count_cpu_percent(proc, children, pro):
    """
    Count all process cpu percent.
    """
    if children:
        for sub_pro in children:
            try:
                child = sub_pro.children()
                chi_per = sub_pro.cpu_percent(interval=0.3)
                pro.cpu_all += chi_per
                mem_use = sub_pro.memory_info().rss
                pro.mem_all += mem_use
                count_cpu_percent(sub_pro, child, pro)
            except Exception as e:
                print(e)
                continue
    else:
        return

def getWatchInfo(pro_id):
    """
    Get cpu all core
    """
    # pro_id = 00022_1dd2bbbd72dd4dcb891f56130b15ca1a_8
    project_name = None
    job_id = None
    require_cpu = None
    if pro_id:
        try:
            infos = pro_id.split('_')
            if infos and len(infos) == 2:
                project_name = infos[0]
                job_id = infos[1]
            elif infos and len(infos) == 3:
                project_name = infos[0]
                job_id = infos[1]
                require_cpu = int(infos[2])
        except Exception as e:
            print(e)
    return project_name, job_id, require_cpu
