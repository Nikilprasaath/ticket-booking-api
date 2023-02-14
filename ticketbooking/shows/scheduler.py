from .models import bookings
import threading
from schedule import Scheduler
from django.utils import timezone
import time
from django.conf import settings

def job():
    now = timezone.now()
    queryset = bookings.objects.filter(status= 'active',show__show_time__lte = now)
    print(queryset)
    for obj in queryset:
        print(obj.status)
        obj.status = 'not active'
        obj.save()


def run_continuously(self, interval=1):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously

scheduler = Scheduler()
scheduler.every(10).minutes.do(job)
scheduler.run_continuously()
