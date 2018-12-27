from rasa_core.interpreter import RasaNLUInterpreter
from rasa.lineagent import LineAgent
from rasa.lineconnector import LineInput

import os

# load your trained agent
agent = LineAgent.load("models/dialogue", interpreter=RasaNLUInterpreter("models/current/nlu"))

line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
port = int(os.getenv('PORT', None))

input_channel = LineInput(
    line_secret=line_secret,
    line_access_token=line_access_token
)

app = agent.handle_channels([input_channel], http_port=port)
