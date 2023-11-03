# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from collectNode import CollectNode

cn = CollectNode()

def collect_node_mem_info():
    cn.collect_node_mem_info()
def collect_node_cpu_info():
    cn.collect_node_cpu_info()
def collect_node_disk_info():
    cn.collect_node_disk_info()

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(collect_node_mem_info, 'interval', seconds=10, id='node_mem')
    sched.add_job(collect_node_cpu_info, 'interval', seconds=10, id='node_cpu')
    sched.add_job(collect_node_disk_info, 'interval', seconds=10, id='node_disk')
    sched.start()
