from flask import Flask
from rasa.line import LineInput
import os
from rasa_core.agent import Agent
from rasa.interpreter import LineEventInterpreter

# load your trained agent
agent = Agent.load("models/dialogue", interpreter=LineEventInterpreter("models/current/nlu"))

line_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
port = int(os.getenv('PORT', None))

input_channel = LineInput(
    line_secret=line_secret,
    line_access_token=line_access_token
)

app = agent.handle_channels([input_channel], http_port=port)
