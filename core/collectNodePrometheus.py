# -*- coding: utf-8 -*-

from nodeinfo import NodeResourceV2
from prometheusClient import push_info
import awsUtil
from prometheus_client import CollectorRegistry, Gauge

# Init node info.
node = NodeResourceV2()

class CollectNode(object):
    """
    Collect node info.
    """
    
    def __init__(self):
        self.instance_meta = awsUtil.get_instance_metadata()

    def collect_node_cpu_info(self):
        """
        Collect host cpu.
        :return:
        """
        instance_id = self.instance_meta.get('instanceId', '')
        instance_type = self.instance_meta.get('instanceType', '')
        cpu_info = node.get_cpu_state()
        
        registry = CollectorRegistry()
                
        g_node_cpu_use_percent = Gauge('node_cpu_use_percent', 'The cpu use of node', ['instance_id', 'instance_type'], registry=registry)
        g_node_cpu_use_percent.labels(instance_id=instance_id, instance_type=instance_type).set(cpu_info.get('cpu_percent'))
        
        g_node_cpu_use_load5 = Gauge('node_cpu_loadavg_5', 'The cpu load 5 use of node', ['instance_id', 'instance_type'], registry=registry)
        g_node_cpu_use_load5.labels(instance_id=instance_id, instance_type=instance_type).set(cpu_info.get('loadavg_5'))
        
        g_node_cpu_use_load10 = Gauge('node_cpu_loadavg_10', 'The cpu load 10 use of node', ['instance_id', 'instance_type'], registry=registry)
        g_node_cpu_use_load10.labels(instance_id=instance_id, instance_type=instance_type).set(cpu_info.get('loadavg_10'))
        
        g_node_cpu_use_load15 = Gauge('node_cpu_loadavg_15', 'The cpu load 15 use of node', ['instance_id', 'instance_type'], registry=registry)
        g_node_cpu_use_load15.labels(instance_id=instance_id, instance_type=instance_type).set(cpu_info.get('loadavg_15'))
        
        push_info('node_cpu_use', registry)
        

    def collect_node_mem_info(self):
        """
        Collect node memory.
        """
        instance_id = self.instance_meta.get('instanceId', '')
        instance_type = self.instance_meta.get('instanceType', '')
        mem_info = node.get_memory_state()
            
        registry = CollectorRegistry()
                
        mem_use = Gauge('mem_used', 'The mem ues of node', ['instance', 'instance_type'], registry=registry)
        mem_use.labels(instance=instance_id, instance_type=instance_type).set(mem_info.get('mem_used'))
        
        mem_per_used = Gauge('mem_used_per', 'The mem use percent of node', ['instance', 'instance_type'], registry=registry)
        mem_per_used.labels(instance=instance_id, instance_type=instance_type).set(mem_info.get('mem_used_per'))
        
        push_info('node_mem_use', registry)
        

    def collect_node_disk_info(self):
        """
        Collect node disk.
        """
        instance_id = self.instance_meta.get('instanceId', '')
        instance_type = self.instance_meta.get('instanceType', '')
        disk_info = node.get_disk_state()
                
        registry = CollectorRegistry()
                
        disk_used = Gauge('disk_used', 'The disk use of node', ['instance', 'instance_type'], registry=registry)
        disk_used.labels(instance=instance_id, instance_type=instance_type).set(disk_info.get('disk_used'))
        
        disk_used_per = Gauge('disk_used_per', 'The disk use percent of node', ['instance', 'instance_type'], registry=registry)
        disk_used_per.labels(instance=instance_id, instance_type=instance_type).set(disk_info.get('disk_used_per'))
        
        push_info('node_disk_use', registry)


if __name__ == '__main__':
    c = CollectNode()
    c.collect_node_cpu_info()
    c.collect_node_mem_info()
    c.collect_node_disk_info()
