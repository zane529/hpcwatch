# -*- coding: utf-8 -*-

from nodeinfo import NodeResource
import slurm.cmdagent as cmdagent
import influxdbClient
import awsUtil

# Init InfluxDB client.
client = influxdbClient.get_influxdb_client()
# Init node info.
node = NodeResource()


def collect_process_info():
    instance_id = awsUtil.get_aws_instance_id()
    instance_type = awsUtil.get_aws_instance_type()
    procs = node.get_process_info()
    for proc in procs:
        pid = proc['pid']
        cpu_info = proc['cpu_info']
        project_name = proc['project_name']
        mem_info = proc['mem_info']
        disk_info = proc['disk_info']
        
        # Collect process cpu info.
        cpu_collects = list()
        cpu_resource = dict()
        cpu_resource['measurement'] = 'proc_cpu_use'
        cpu_tags = dict()
        cpu_tags['host'] = instance_id
        cpu_tags['instance_type'] = instance_type
        cpu_tags['pid'] = pid
        if project_name:
            cpu_tags['project_name'] = project_name
        cpu_resource['tags'] = cpu_tags
        cpu_fields = cpu_info
        cpu_resource['fields'] = cpu_fields
        cpu_collects.append(cpu_resource)
        client.write_points(cpu_collects)

        # Collect process mem info.
        mem_collects = list()
        mem_resource = dict()
        mem_resource['measurement'] = 'proc_mem_use'
        mem_tags = dict()
        mem_tags['host'] = instance_id
        mem_tags['instance_type'] = instance_type
        mem_tags['pid'] = pid
        if project_name:
            mem_tags['project_name'] = project_name
        mem_resource['tags'] = mem_tags
        mem_fields = mem_info
        mem_resource['fields'] = mem_fields
        mem_collects.append(mem_resource)
        client.write_points(mem_collects)

        # Collect process disk info.
        if disk_info:
            disk_collects = list()
            disk_resource = dict()
            disk_resource['measurement'] = 'proc_disk_use'
            disk_tags = dict()
            disk_tags['host'] = instance_id
            disk_tags['instance_type'] = instance_type
            disk_tags['pid'] = pid
            if project_name:
                disk_tags['project_name'] = project_name
            disk_resource['tags'] = disk_tags
            disk_fields = disk_info
            disk_resource['fields'] = disk_fields
            disk_collects.append(disk_resource)
            client.write_points(disk_collects)

if __name__ == '__main__':
    collect_process_info()