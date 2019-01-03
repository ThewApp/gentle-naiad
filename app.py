import argparse
import logging
import os

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

logging.basicConfig(level=logging_level)

logger = logging.getLogger(__name__)

from rasa_core.interpreter import RasaNLUInterpreter
from rasa.lineagent import LineAgent
from rasa.lineconnector import LineInput
from rasa.store import tracker_store


agent = LineAgent.load(
    "models/dialogue",
    interpreter=RasaNLUInterpreter("models/current/nlu"),
    tracker_store=tracker_store
)

def webapp():
    line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    port = int(os.getenv('PORT', 8080))

    input_channel = LineInput(
        line_secret=line_secret,
        line_access_token=line_access_token
    )

    logger.info("Web is ready.")

    agent.handle_channels([input_channel], http_port=port)

def worker():
    from multiprocessing import Process
    from rasa.store import scheduler_store
    from rasa.worker import ReminderJob, ReminderWorker
    from rq import Worker, Queue, Connection
    from rq_scheduler.scheduler import Scheduler

    listen = ['high', 'default', 'low']
    scheduler = Scheduler(
        connection=scheduler_store,
        interval=5
    )
    Process(target=scheduler.run).start()
    with Connection(scheduler_store):
        worker = ReminderWorker(map(Queue, listen))
        Process(target=worker.work).start()
    logger.info("Worker is ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MeDiary Application')
    parser.add_argument('type', default="web", help='Process type')

    args = parser.parse_args()
    if args.type == "web":
        logger.debug("Starting web app")
        webapp()
    elif args.type == "worker":
        logger.debug("Starting worker app")
        worker()
