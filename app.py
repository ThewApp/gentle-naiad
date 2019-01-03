from rasa_core.interpreter import RasaNLUInterpreter
from rasa.lineagent import LineAgent
from rasa.lineconnector import LineInput
from rasa.store import tracker_store, scheduler_store
from rq import Worker, Queue, Connection
from rq_scheduler.scheduler import Scheduler
from multiprocessing import Process

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

line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

agent = LineAgent.load(
    "models/dialogue",
    interpreter=RasaNLUInterpreter("models/current/nlu"),
    tracker_store=tracker_store
)

def webapp():
    port = int(os.getenv('PORT', 8080))

    input_channel = LineInput(
        line_secret=line_secret,
        line_access_token=line_access_token
    )

    logger.info("Web is ready.")

    agent.handle_channels([input_channel], http_port=port)

def worker():
    listen = ['high', 'default', 'low']
    scheduler = Scheduler(
        connection=scheduler_store,
        interval=5
    )
    Process(target=scheduler.run).start()
    with Connection(scheduler_store):
        worker = Worker(map(Queue, listen))
        Process(target=worker.work).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MeDiary Application')
    parser.add_argument('type', default="web", help='Process type')

    args = parser.parse_args()
    if args.type == "web":
        webapp()
    elif args.type == "worker":
        worker()
