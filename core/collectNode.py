# -*- coding: utf-8 -*-

from nodeinfo import NodeResource
import influxdbClient
import awsUtil

# Init InfluxDB client.
client = influxdbClient.get_influxdb_client()
# Init node info.
node = NodeResource()

class CollectNode(object):
    """
    Collect node info.
    """

    def collect_node_cpu_info(self):
        """
        Collect host cpu.
        :return:
        """
        instance_id = awsUtil.get_aws_instance_id()
        instance_type = awsUtil.get_aws_instance_type()
        cpu_info = node.get_cpu_state()
        collects = list()
        resource = dict()
        resource['measurement'] = 'node_cpu_use'
        tags = dict()
        tags['host'] = instance_id
        tags['instance_type'] = instance_type
        resource['tags'] = tags
        fields = cpu_info
        resource['fields'] = fields
        collects.append(resource)
        client.write_points(collects)

    def collect_node_mem_info(self):
        """
        Collect node memory.
        """
        instance_id = awsUtil.get_aws_instance_id()
        instance_type = awsUtil.get_aws_instance_type()
        mem_info = node.get_memory_state()
        collects = list()
        resource = dict()
        resource['measurement'] = 'node_mem_use'
        tags = dict()
        tags['host'] = instance_id
        tags['instance_type'] = instance_type
        resource['tags'] = tags
        fields = mem_info
        resource['fields'] = fields
        collects.append(resource)
        client.write_points(collects)

    def collect_node_disk_info(self):
        """
        Collect node disk.
        """
        instance_id = awsUtil.get_aws_instance_id()
        instance_type = awsUtil.get_aws_instance_type()
        disk_info = node.get_disk_state()
        collects = list()
        resource = dict()
        resource['measurement'] = 'node_disk_use'
        tags = dict()
        tags['host'] = instance_id
        tags['instance_type'] = instance_type
        resource['tags'] = tags
        fields = disk_info
        resource['fields'] = fields
        collects.append(resource)
        client.write_points(collects)


if __name__ == '__main__':
    c = CollectNode()
    c.collect_node_cpu_info()
    c.collect_node_mem_info()
    c.collect_node_disk_info()
