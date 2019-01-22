import logging
import os
from multiprocessing import Process

from rasa_core.interpreter import RasaNLUInterpreter
from rq import Connection, Queue, Worker
from rq_scheduler.scheduler import Scheduler

import app.logging
from app.rich_menu import RichMenu
from app.scheduling import ReminderJob, ReminderWorker
from rasa.lineagent import LineAgent
from rasa.store import scheduler_store, tracker_store

logger = logging.getLogger(__name__)

logger.debug("Starting worker")

line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
rich_menu = RichMenu(line_access_token)
rich_menu.setup()

agent = LineAgent.load(
    "models/dialogue",
    interpreter=RasaNLUInterpreter("models/current/nlu"),
    tracker_store=tracker_store
)

workerKwargs = {
    "rich_menu": rich_menu,
    "agent": agent
}

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
    worker.work(workerKwargs=workerKwargs)
