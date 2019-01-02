from rasa.store import scheduler_store
from rq import Worker, Queue, Connection
from rq_scheduler.scheduler import Scheduler
import threading

from rq_scheduler.utils import setup_loghandlers

setup_loghandlers('DEBUG')

listen = ['high', 'default', 'low']

if __name__ == '__main__':
    scheduler = Scheduler(
        connection=scheduler_store,
        interval=5
    )
    running_scheduler = threading.Thread(target=scheduler.run)
    running_scheduler.start()
    with Connection(scheduler_store):
        worker = Worker(map(Queue, listen))
        worker.work()
