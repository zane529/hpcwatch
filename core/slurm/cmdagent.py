# -*- coding: utf-8 -*-

import subprocess

def get_slurm_jobs(nodelist):
    """
    Get slurm jobs.
    :param nodelist:
    :return:
    """
    # squeue -h -o "%i,%N" | grep node-1
    command = 'squeue -h -o "%i,%N" | grep ' + nodelist
    print(command)
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    lines = output.strip().split('\n')
    jobs = []
    for line in lines:
        data = line.split(',')
        job = data[0]
        jobs.append(job)
    return jobs

def get_pid_by_jobid(job_id):
    """
    Get pid by jobid.
    :param job_id:
    :return:
    """
    result = None
    command = "ps -ef | grep %s.batch | grep -v grep | awk '{print $2}'" % job_id
    print(command)
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    if output:
        result = output.rstrip("\n")
    return result

def get_job_workdir(jobid):
    """
    Get job workdir.
    :param jobid:
    :return:
    """
    result = None
    command = "scontrol show job %s | grep -E 'WorkDir' | awk -F= '{print $2}' | awk '{$1=$1};1'" % jobid
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    if output:
        result = output.rstrip("\n")
    return result
