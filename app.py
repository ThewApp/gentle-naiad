from rasa_core.interpreter import RasaNLUInterpreter
from rasa.lineagent import LineAgent
from rasa.lineconnector import LineInput

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
    logging_level = logging.INFO

logging.basicConfig(level=logging_level)

logger = logging.getLogger(__name__)

# load your trained agent
agent = LineAgent.load(
    "models/dialogue", interpreter=RasaNLUInterpreter("models/current/nlu"))

line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
port = int(os.getenv('PORT', None))

input_channel = LineInput(
    line_secret=line_secret,
    line_access_token=line_access_token
)

logger.info("Ready")

app = agent.handle_channels([input_channel], http_port=port)
