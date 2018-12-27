from rasa_core.dispatcher import Dispatcher

from collections import namedtuple
from typing import Text, List, Optional, Callable, Any, Dict, Union

BotMessage = namedtuple("BotMessage", "text data")


class LineDispatcher(Dispatcher):
    def line_response(self, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""

        self.output_channel.send_response(self.sender_id, message)

    def line_template(self,
                      template: Text,
                      tracker: 'DialogueStateTracker',
                      **kwargs: Any
                      ) -> None:
        """"Send a message to the client based on a template."""

        message = self.nlg.generate(template, tracker, **kwargs)

        print(message)

        if not message:
            return

        if type(message) == list:
            for item in message:
                self.line_response(item)
        else:
            self.line_response(message)