from subprocess import call
from apscheduler.schedulers.blocking import BlockingScheduler

"""
sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10)
def timed_job():
    call(["python", "manage.py", "youtube"])


sched.start()
"""
