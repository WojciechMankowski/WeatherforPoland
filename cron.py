import sched
import time
from main import run_example
from apscheduler.schedulers.blocking import BlockingScheduler

s = sched.scheduler(time.time, time.sleep)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def RunExample():
    run_example()

RunExample()
sched.start()

