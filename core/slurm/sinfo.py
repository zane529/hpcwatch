# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from time import mktime
from ClusterShell.Task import task_self, TimeoutError
from ClusterShell.Event import EventHandler
sys.path.append("..")
# import influxdbClient

_result = dict()

# Init InfluxDB client.
# client = influxdbClient.get_influxdb_client()


def strdate_to_ts(s):
    """
    Helper function to convert human readable sdiag date into timestamp
    """
    return int(mktime(
        datetime.strptime(s.strip(), "%a %b %d %H:%M:%S %Y").timetuple()))


class SInfoHdlr(EventHandler):
    """ClusterShell event handler for sinfo command execution."""

    def __init__(self):
        """initalizer: compile regexp pattern used to parse sinfo output"""
        self.pattern = re.compile(
            r"(?P<partition>.*)\s(?P<mem>\d*)\s(?P<cpu>\d*)\s"
            r"(?P<features>.*)\s(?P<gres>.*)\s"
            r"(?P<state>[^*$~#]*)[*$~#]?\s(?P<nodecnt>\d*)\s"
            r"(?P<allocated>\d*)/(?P<idle>\d*)/(?P<other>\d*)/(?P<total>\d*)")
        self.transtable = {ord("."): "_", ord("*"): ""}
        self.remove_star = {ord("*"): ""}
        self.partitions = set()
        self.nodes = {}
        self.nodes_total = {}
        self.cpus = {}
        self.cpus_total = {}

    def ev_read(self, worker):
        """read line from sinfo command"""
        # owners 64000 16 CPU_IVY,E5-2650v2,2.60GHz,GPU_KPL,TITAN_BLACK,titanblack gpu:gtx:4 mixed 2 8/24/0/32
        msg = str(worker.current_msg, 'UTF-8')
        match = self.pattern.match(msg)
        if match:
            # get partition name (cleaned) and add to a set for partition_count
            partition = match.group("partition").translate(self.remove_star)
            self.partitions.add(partition)
            features = match.group("features").translate(self.transtable)
            gres = match.group("gres")
            # build path
            base_path = "sinfo.%s.%s.%s.%s.%s" % (partition,
                                                  match.group("mem"), match.group(
                                                      "cpu"), features,
                                                  re.sub('[()]', '', gres))
            print(base_path)

            # build dicts to handle any duplicates and also total...

            # nodes
            state = match.group("state")
            nodecnt = int(match.group("nodecnt"))

            if base_path not in self.nodes:
                self.nodes[base_path] = {'allocated': 0, 'completing': 0,
                                         'down': 0, 'drained': 0,
                                         'draining': 0, 'idle': 0,
                                         'maint': 0, 'mixed': 0, 'unknown': 0, 'idle~': 0}
                self.nodes[base_path][state] = 0  # in case of another state
                self.nodes_total[base_path] = 0

            self.nodes_total[base_path] += nodecnt

            try:
                self.nodes[base_path][state] += nodecnt
            except KeyError:
                self.nodes[base_path][state] = nodecnt

            # CPUs
            if base_path not in self.cpus:
                self.cpus[base_path] = {'allocated': 0,
                                        'idle': 0,
                                        'other': 0}
                self.cpus_total[base_path] = 0

            for cpustate in ('allocated', 'idle', 'other'):
                self.cpus[base_path][cpustate] += int(match.group(cpustate))

            self.cpus_total[base_path] += int(match.group('total'))

    def ev_close(self, worker):
        pass


def main():
    # Get clustershell task object
    task = task_self()
    task.set_default('stdout_msgtree', False)
    task.shell("sinfo -h -e -o '%R %m %c %f %G %T %D %C'",
               handler=SInfoHdlr(), stderr=True)
    task.resume(timeout=30)
    # if _result and len(_result) > 0:
    #     sdiag_collects = list()
    #     sdiag_resource = dict()
    #     sdiag_resource['measurement'] = 'slurm_sdiag'
    #     sdiag_resource['fields'] = _result
    #     sdiag_collects.append(sdiag_resource)
    #     client.write_points(sdiag_collects)


if __name__ == '__main__':
    # pattern = re.compile(
    #         r"(?P<partition>.*)\s(?P<mem>\d*)\s(?P<cpu>\d*)\s"
    #         r"(?P<features>.*)\s(?P<gres>.*)\s"
    #         r"(?P<state>[^*$~#]*)[*$~#]?\s(?P<nodecnt>\d*)\s"
    #         r"(?P<allocated>\d*)/(?P<idle>\d*)/(?P<other>\d*)/(?P<total>\d*)")
    # msg = 't2micro* 972 1 dynamic,t2.micro,t2micro (null) idle~ 19 0/19/0/19'
    # match = pattern.match(msg)

    # partition = match.group("partition").translate({ord("*"): ""})
    # print(partition)
    main()
