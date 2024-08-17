# -*- coding: utf-8 -*-

from nodeinfo import NodeResourceV2
import slurm.cmdagent as cmdagent
from prometheusClient import push_info
import awsUtil
from prometheus_client import CollectorRegistry, Gauge
import time, uuid

# Init node info.
node = NodeResourceV2()


def collect_process_info():

    start_time = time.time()

    run_id = 'Processs-' + str(uuid.uuid4())[:8]
    
    instance_meta = awsUtil.get_instance_metadata()
    
    instance_id = instance_meta.get('instanceId', '')
    instance_type = instance_meta.get('instanceType', '')
    
    hostname_dict = node.get_host_info()
    jobs = cmdagent.get_slurm_jobs(hostname_dict.get('host_name', None))
    
    
    
    for job in jobs:
        job_id = job.get_job_id()
        job_name = job.get_job_name()
        project_name = ''
        if job_name:
            if '_' in job_name:
                project_name = job_name.split('_')[0]
        workdir = cmdagent.get_job_workdir(job_id)
        pid = cmdagent.get_pid_by_jobid(job_id)
        proc = node.get_process_info_by_id(pid, workdir)

        if proc is None:
            continue

        cpu_info = proc['cpu_info']
        
        mem_info = proc['mem_info']
        disk_info = proc['disk_info']

        pid = job_id + '_' + pid

        registry = CollectorRegistry()

        # Collect process cpu info.
        cpu_use = cpu_info.get('cpu_use')
        proc_cpu_use = Gauge('proc_cpu_use', 'The cpu use of job', ['instance_id', 'instance_type', 'project_name'], registry=registry)
        proc_cpu_use.labels(instance=pid, instance_id=instance_id, instance_type=instance_type, project_name=project_name).set(cpu_use)

        # Collect process mem info.
        mem_use = mem_info.get('mem_use')
        proc_mem_use = Gauge('proc_mem_use', 'The mem use of job', ['instance', 'instance_id', 'instance_type', 'project_name'], registry=registry)
        proc_mem_use.labels(instance=pid, instance_id=instance_id, instance_type=instance_type, project_name=project_name).set(mem_use)

        # Collect process disk info.
        if disk_info:
            disk_use = disk_info.get('disk_use')
            proc_disk_use = Gauge('proc_disk_use', 'The disk use of job', ['instance', 'instance_id', 'instance_type', 'project_name'], registry=registry)
            proc_disk_use.labels(instance=pid, instance_id=instance_id, instance_type=instance_type, project_name=project_name).set(disk_use)

        if any(registry.collect()):
            i_p_uuid = instance_id + '_' + pid
            push_info('job_info', registry, i_p_uuid)
        else:
            print("No metrics to push, registry is empty")

    end_time = time.time()

    print(f"[{run_id}] executed in {end_time - start_time:.4f} seconds")
    print('-' * 200)


if __name__ == '__main__':
    collect_process_info()