# -*- coding: utf-8 -*-

class JobInfo(object):
    job_id = None
    job_name = None

    def __init__(self, job_id, job_name):
        self.job_id = job_id
        self.job_name = job_name
    
    def get_job_id(self):
        return self.job_id
    
    def set_job_id(self, job_id):
        self.job_id = job_id

    def get_job_name(self):
        return self.job_name
    
    def set_job_name(self, job_name):
        self.job_name = job_name

    def __str__(self):
        return "job_id: " + str(self.job_id) + " job_name: " + self.job_name