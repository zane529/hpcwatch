# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from time import mktime
from ClusterShell.Task import task_self, TimeoutError
from ClusterShell.Event import EventHandler
sys.path.append("..")
import influxdbClient

_result = dict()

# Init InfluxDB client.
client = influxdbClient.get_influxdb_client()

def str_to_int(s):
    """
    Convert string to int.
    """
    try:
        return int(s)
    except Exception as e:
        return 

def strdate_to_ts(s):
    """
    Helper function to convert human readable sdiag date into timestamp
    """
    return int(mktime(
        datetime.strptime(s.strip(), "%a %b %d %H:%M:%S %Y").timetuple()))


class SDiagHdlr(EventHandler):
    """ClusterShell event handler for sdiag command execution."""

    def __init__(self):
        """initializer: compile regexp used to parse sdiag output"""
        self.section = "sdiag"
        self.root_patterns = {
            # Server thread count: 5
            # Agent queue size:    0
            # Jobs submitted: 2915
            # Jobs started:   1707
            # Jobs completed: 1653
            # Jobs canceled:  20
            # Jobs failed:    0
            'thread_count':     re.compile(r"Server thread count:\s*(?P<thread_count>\d*)"),
            'agent_queue_size': re.compile(r"Agent queue size:\s*(?P<agent_queue_size>\d*)"),
            'jobs.submitted':   re.compile(r"Jobs submitted:\s*(?P<submitted>\d*)"),
            'jobs.started':     re.compile(r"Jobs started:\s*(?P<started>\d*)"),
            'jobs.completed':   re.compile(r"Jobs completed:\s*(?P<completed>\d*)"),
            'jobs.canceled':    re.compile(r"Jobs canceled:\s*(?P<canceled>\d*)"),
            'jobs.failed':      re.compile(r"Jobs failed:\s*(?P<failed>\d*)"),
            'data_since':      (re.compile(r"Data since\s*(?P<data_since>\w+\s+\w+\s+\d+\s+\d+[:]\d+[:]\d+\s+\d+)\s*.*"), strdate_to_ts),
        }
        self.sched_main_patterns = {
            # Last cycle:   11079
            # Max cycle:    123872
            # Total cycles: 2724
            # Mean cycle:   17276
            # Mean depth cycle:  314
            # Cycles per minute: 13
            # Last queue length: 2176
            'last_cycle_usec': re.compile(r"\s*Last cycle:\s*(?P<last_cycle_usec>\d*)"),
            'max_cycle_usec': re.compile(r"\s*Max cycle:\s*(?P<max_cycle_usec>\d*)"),
            'total_cycles': re.compile(r"\s*Total cycles:\s*(?P<total_cycles>\d*)"),
            'mean_cycle_usec': re.compile(r"\s*Mean cycle:\s*(?P<mean_cycle_usec>\d*)"),
            'mean_depth_cycle': re.compile(r"\s*Mean depth cycle:\s*(?P<mean_depth_cycle>\d*)"),
            'cycles_per_minute': re.compile(r"\s*Cycles per minute:\s*(?P<cycles_per_minute>\d*)"),
            'last_queue_length': re.compile(r"\s*Last queue length:\s*(?P<last_queue_length>\d*)"),
        }
        self.sched_backfill_patterns = {
            # Total backfilled jobs (since last slurm start): 3310
            # Total backfilled jobs (since last stats cycle start): 102
            # Total cycles: 289
            # Last cycle when: Sun Jun 21 19:42:02 2015
            # Last cycle: 2513675311
            # Mean cycle: 7318652
            # Last depth cycle: 2534
            # Last depth cycle (try sched): 60
            # Depth Mean: 3024
            # Depth Mean (try depth): 62
            # Last queue length: 2713
            # Queue length mean
            'total_bf_jobs': re.compile(r"\s*Total backfilled jobs \(since last slurm start\):\s*(?P<total_bf_jobs>\d*)"),
            'total_bf_jobs_since_reset': re.compile(r"\s*Total backfilled jobs \(since last stats cycle start\):\s*(?P<total_bf_jobs_since_reset>\d*)"),
            'total_cycles': re.compile(r"\s*Total cycles:\s*(?P<total_cycles>\d*)"),
            'last_cycle_time': (re.compile(r"Last cycle when:\s*(?P<last_cycle_time>\w+\s+\w+\s+\d+\s+\d+[:]\d+[:]\d+\s+\d+)\s*.*"), strdate_to_ts),
            'last_cycle_usec': re.compile(r"\s*Last cycle:\s*(?P<last_cycle_usec>\d*)"),
            'last_mean_cycle_usec': re.compile(r"\s*Mean cycle:\s*(?P<last_mean_cycle_usec>\d*)"),
            'last_depth_cycle': re.compile(r"\s*Last depth cycle:\s*(?P<last_depth_cycle>\d*)"),
            'last_depth_cycle_try': re.compile(r"\s*Last depth cycle \(try sched\):\s*(?P<last_depth_cycle_try>\d*)"),
            'depth_mean': re.compile(r"\s*Depth Mean:\s*(?P<depth_mean>\d*)"),
            'depth_mean_try': re.compile(r"\s*Depth Mean \(try depth\):\s*(?P<depth_mean_try>\d*)"),
            'bf_last_queue_length': re.compile(r"\s*Last queue length:\s*(?P<bf_last_queue_length>\d*)"),
            'queue_length_mean': re.compile(r"\s*Queue length mean:\s*(?P<queue_length_mean>\d*)"),
        }

    def ev_read(self, worker):
        """read line from sinfo command"""
        msg = str(worker.current_msg, 'UTF-8')
        # Look at sdiag section change
        if msg.startswith("Main schedule statistics"):
            self.section = "sdiag.scheduler.main"
        elif msg.startswith("Backfilling stats"):
            self.section = "sdiag.scheduler.backfill"

        # Handle section specific content
        if self.section == "sdiag":
            for key, pat in self.root_patterns.items():
                if type(pat) is tuple:  # include post-convert function?
                    pat, fun = pat
                else:
                    def fun(x): return x
                match = pat.match(msg)
                if match:
                    _result[key] = str_to_int(fun(match.group(key.split('.')[-1])))

        elif self.section == "sdiag.scheduler.main":
            for key, pat in self.sched_main_patterns.items():
                match = pat.match(msg)
                if match:
                    
                    _result[key] = str_to_int(match.group(key))

        elif self.section == "sdiag.scheduler.backfill":
            for key, pat in self.sched_backfill_patterns.items():
                if type(pat) is tuple:  # include post-convert function?
                    pat, fun = pat
                else:
                    def fun(x): return x
                match = pat.match(msg)
                if match:
                    _result[key] = str_to_int(fun(match.group(key)))


def main():
    # Get clustershell task object
    task = task_self()
    task.set_default('stdout_msgtree', False)
    task.shell("sdiag", handler=SDiagHdlr(), stderr=True)
    task.resume(timeout=30)
    if _result and len(_result) > 0:
        sdiag_collects = list()
        sdiag_resource = dict()
        sdiag_resource['measurement'] = 'slurm_sdiag'
        sdiag_resource['fields'] = _result
        sdiag_collects.append(sdiag_resource)
        client.write_points(sdiag_collects)
