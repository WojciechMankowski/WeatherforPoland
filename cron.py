import sched
import time
from main import run_example
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

s = sched.scheduler(time.time, time.sleep)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def RunExample():
    Time = datetime.datetime.now().time()
    print(Time)
    run_example()

RunExample()
sched.start()

