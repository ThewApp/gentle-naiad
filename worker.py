from rasa.store import scheduler_store
from rq import Worker, Queue, Connection
from rq_scheduler.scheduler import Scheduler
from multiprocessing import Process

listen = ['high', 'default', 'low']

if __name__ == '__main__':
    scheduler = Scheduler(
        connection=scheduler_store,
        interval=5
    )
    Process(target=scheduler.run).start()
    with Connection(scheduler_store):
        worker = Worker(map(Queue, listen))
        Process(target=worker.work).start()
