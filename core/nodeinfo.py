# -*- coding: utf-8 -*-
import os
import socket
import psutil
import awsUtil
from processinfo import ProcInfo

PROCESS_KEY = '--watch-id='
DISK_PATH = awsUtil.get_aws_parameter('JobPrefixPath')


class NodeResourceV2(object):
    """
    Get node resources, like cpu, mem, disk, instanceId.
    """

    def get_host_info(self):
        """
        Get hostname.
        :return:
        """
        host_name = socket.gethostname()
        return {'host_name': host_name}

    def get_cpu_state(self):
        """
        Get cpu info.
        :return:
        """
        cpu_percent = awsUtil.to_int(psutil.cpu_percent())
        loadavg = psutil.getloadavg()
        return {'cpu_percent': cpu_percent, 'loadavg_5': awsUtil.to_int(loadavg[0]), 'loadavg_10': awsUtil.to_int(loadavg[1]), 'loadavg_15': awsUtil.to_int(loadavg[2])}

    def get_memory_state(self):
        """
        Get memory info.
        :return:
        """
        mem = psutil.virtual_memory()
        mem_used = mem.used
        mem_used_per = mem.percent
        i_mem_used = 0
        i_mem_per_used = 0
        try:
            i_mem_used = awsUtil.to_int(mem_used))
            i_mem_per_used = awsUtil.to_int(mem_used_per)
        except Exception as e:
            print(e)
        return {'mem_used': i_mem_used, 'mem_used_per': i_mem_per_used}

    def get_disk_state(self):
        """
        Get disk info.
        :return:
        """
        diskpath = '/'
        disk_stat = psutil.disk_usage(diskpath)
        disk_used = disk_stat.used
        disk_used_per = disk_stat.percent
        i_disk_used = 0
        i_disk_per_used = 0
        
        try:
            i_disk_used = awsUtil.to_int(disk_used)
            i_disk_per_used = awsUtil.to_int(disk_used_per)
        except Exception as e:
            print(e)
        return {'disk_used': i_disk_used, 'disk_used_per': i_disk_per_used}
    
    def get_process_info_by_id(self, pid, workdir):
        """
        Get the process info by id.
        """

        pro_info = None
        if pid:
            try:
                pid = int(pid)
                project_name = ""
                proc = psutil.Process(pid)
                pro_tmp = ProcInfo()
                children = proc.children()
                awsUtil.count_cpu_percent(proc, children, pro_tmp)
                mem_info = {'mem_use': awsUtil.to_int(pro_tmp.mem_all)}
                cpu_use = pro_tmp.cpu_all
                cpu_info = {'cpu_use': awsUtil.to_int(cpu_use)}
                # Collect disk info.
                disk_info = None
                if os.path.exists(workdir):
                    disk_size = 0
                    disk_used = awsUtil.getFileSize(workdir, disk_size)
                    disk_info = {'disk_use': awsUtil.to_int(disk_used)}    
                pro_info = {'pid': pid, 'cpu_info': cpu_info, 'mem_info': mem_info,
                            'disk_info': disk_info, 'project_name': project_name}
            except Exception as e:
                print(e)            
        return pro_info

    def get_process_info(self):
        """
        Get the process info.
        """

        hostname = self.get_host_info()

        result = list()
        for proc in psutil.process_iter():
            pro_cmd = proc.cmdline()
            if pro_cmd and len(pro_cmd) > 0:
                job_name = pro_cmd[-1]
                if job_name.startswith(PROCESS_KEY):
                    pro_id = job_name[len(PROCESS_KEY):]
                    # sbatch require -c value.
                    project_name, job_id, require_cpus = awsUtil.getWatchInfo(
                        pro_id)
                    pro_tmp = ProcInfo()
                    children = proc.children()
                    awsUtil.count_cpu_percent(proc, children, pro_tmp)
                    mem_info = {'mem_use': awsUtil.to_int(pro_tmp.mem_all)}
                    cpu_use = pro_tmp.cpu_all
                    cpu_percent = cpu_use
                    if require_cpus and require_cpus > 0:
                        cpu_percent = cpu_use//require_cpus
                    r_cpu_info = 0
                    try:
                        r_cpu_info = awsUtil.to_int(cpu_percent)
                    except Exception as e:
                        r_cpu_info = 0
                    cpu_info = {'cpu_use': awsUtil.to_int(r_cpu_info)}
                    # Collect disk info.
                    disk_info = None
                    if DISK_PATH:
                        disk_path = os.path.join(DISK_PATH, str(pro_id))
                        if os.path.exists(disk_path):
                            disk_size = 0
                            disk_used = awsUtil.getFileSize(
                                disk_path, disk_size)
                            disk_info = {'disk_use': awsUtil.to_int(disk_used)}

                    pro_info = {'pid': pro_id, 'cpu_info': cpu_info, 'mem_info': mem_info,
                                'disk_info': disk_info, 'project_name': project_name}
                    result.append(pro_info)
            else:
                continue
        return result

class NodeResource(object):
    """
    Get node resources, like cpu, mem, disk, instanceId.
    """

    def get_host_info(self):
        """
        Get hostname.
        :return:
        """
        host_name = socket.gethostname()
        return {'host_name': host_name}

    def get_cpu_state(self):
        """
        Get cpu info.
        :return:
        """
        cpu_percent = awsUtil.to_int(psutil.cpu_percent())
        loadavg = psutil.getloadavg()
        return {'cpu_percent': cpu_percent, 'loadavg_5': awsUtil.to_int(loadavg[0]), 'loadavg_10': awsUtil.to_int(loadavg[1]), 'loadavg_15': awsUtil.to_int(loadavg[2])}

    def get_memory_state(self):
        """
        Get memory info.
        :return:
        """
        mem = psutil.virtual_memory()
        mem_used = mem.used
        mem_used_per = mem.percent
        i_mem_used = 0
        i_mem_per_used = 0
        try:
            i_mem_used = awsUtil.to_int(mem_used)
            i_mem_per_used = awsUtil.to_int(mem_used_per)
        except Exception as e:
            print(e)
        return {'mem_used': i_mem_used, 'mem_used_per': i_mem_per_used}

    def get_disk_state(self):
        """
        Get disk info.
        :return:
        """
        diskpath = '/'
        disk_stat = psutil.disk_usage(diskpath)
        disk_used = disk_stat.percent
        i_disk_used = 0
        try:
            i_disk_used = awsUtil.to_int(disk_used)
        except Exception as e:
            print(e)
        return {'disk_used': i_disk_used}

    def get_process_info(self):
        """
        Get the process info.
        """
        result = list()
        for proc in psutil.process_iter():
            pro_cmd = proc.cmdline()
            if pro_cmd and len(pro_cmd) > 0:
                job_name = pro_cmd[-1]
                if job_name.startswith(PROCESS_KEY):
                    pro_id = job_name[len(PROCESS_KEY):]
                    # sbatch require -c value.
                    project_name, job_id, require_cpus = awsUtil.getWatchInfo(
                        pro_id)
                    pro_tmp = ProcInfo()
                    children = proc.children()
                    awsUtil.count_cpu_percent(proc, children, pro_tmp)
                    mem_info = {'mem_use': pro_tmp.mem_all}
                    cpu_use = pro_tmp.cpu_all
                    cpu_percent = cpu_use
                    if require_cpus and require_cpus > 0:
                        cpu_percent = cpu_use//require_cpus
                    r_cpu_info = 0
                    try:
                        r_cpu_info = awsUtil.to_int(cpu_percent)
                    except Exception as e:
                        r_cpu_info = 0
                    cpu_info = {'cpu_use': r_cpu_info}
                    # Collect disk info.
                    disk_info = None
                    if DISK_PATH:
                        disk_path = os.path.join(DISK_PATH, str(pro_id))
                        if os.path.exists(disk_path):
                            disk_size = 0
                            disk_used = awsUtil.getFileSize(
                                disk_path, disk_size)
                            disk_info = {'disk_use': awsUtil.to_int(disk_used)}

                    pro_info = {'pid': pro_id, 'cpu_info': cpu_info, 'mem_info': mem_info,
                                'disk_info': disk_info, 'project_name': project_name}
                    result.append(pro_info)
            else:
                continue
        return result
