# -*- coding: utf-8 -*-

class ProcInfo(object):
    pid = None
    cpu_percent = 0
    cpu_all = 0
    mem_use = 0
    mem_all = 0

    def __init__(self):
        self.pid = None
        self.cpu_percent = 0
        self.cpu_all = 0
        self.mem_use = 0
        self.mem_all = 0