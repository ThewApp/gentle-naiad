import logging
from multiprocessing import Process

from rasa_core.interpreter import RasaNLUInterpreter
from rq import Connection, Queue, Worker
from rq_scheduler.scheduler import Scheduler

import app.logging
from app.scheduling import ReminderJob, ReminderWorker
from rasa.lineagent import LineAgent
from rasa.store import scheduler_store, tracker_store

logger = logging.getLogger(__name__)

logger.debug("Starting worker")

agent = LineAgent.load(
    "models/dialogue",
    interpreter=RasaNLUInterpreter("models/current/nlu"),
    tracker_store=tracker_store
)

listen = ['high', 'default', 'low']
scheduler = Scheduler(
    connection=scheduler_store,
    interval=60,
    job_class=ReminderJob
)
Process(target=scheduler.run).start()
with Connection(scheduler_store):
    worker = ReminderWorker(map(Queue, listen), job_class=ReminderJob)
    logger.info("Worker is ready.")
    worker.work(agent=agent)
