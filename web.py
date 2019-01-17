import logging
import os

from flask import Flask
from rasa_core.channels import channel
from rasa_core.interpreter import RasaNLUInterpreter

import app.logging
from rasa.lineagent import LineAgent
from rasa.lineconnector import LineInput
from rasa.store import scheduler_store, tracker_store

logger = logging.getLogger(__name__)

line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

agent = LineAgent.load(
    "models/dialogue",
    interpreter=RasaNLUInterpreter("models/current/nlu"),
    tracker_store=tracker_store
)

line_input_channel = LineInput(
    line_secret=line_secret,
    line_access_token=line_access_token
)

app = Flask(__name__)
channel.register([line_input_channel],
                 app,
                 agent.handle_message,
                 route="/webhooks/")

logger.info("Web is ready.")
