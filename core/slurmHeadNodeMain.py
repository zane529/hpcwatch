# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from slurm import sdiag


def collect_slurm_sdiag():
    try:
        sdiag.main()
    except Exception as e:
        print('Call slurm sdiag scheduler error.')
        print(e)


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(collect_slurm_sdiag, 'interval',
                  seconds=30, id='slurm_sdiag')
    sched.start()
