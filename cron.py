import sched
import time
from main import run2
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

s = sched.scheduler(time.time, time.sleep)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def run_example():
    Time = datetime.datetime.now().time()
    print(Time)
    run2()

run_example()
sched.start()

