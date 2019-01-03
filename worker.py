from rasa.store import scheduler_store
from rq import Worker, Queue, Connection
from rq_scheduler.scheduler import Scheduler
from multiprocessing import Process

import os
import logging

ENV = os.getenv('ENV', 'PRODUCTION')

if ENV == "LOCAL_DEVELOPMENT":
    logging_level = logging.DEBUG

    import ptvsd
    # 5678 is the default attach port in the VS Code debug configurations
    print("Waiting for debugger attach")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
elif ENV == "DEVELOPMENT":
    logging_level = logging.DEBUG
elif ENV == "STAGING":
    logging_level = logging.INFO
else:
    logging_level = None

logger = logging.getLogger(__name__)

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
