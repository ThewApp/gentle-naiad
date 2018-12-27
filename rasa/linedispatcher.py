from rasa_core.dispatcher import Dispatcher

from collections import namedtuple
from typing import Text, List, Optional, Callable, Any, Dict, Union

BotMessage = namedtuple("BotMessage", "text data")


class LineDispatcher(Dispatcher):
    def line_response(self, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""

        bot_message = BotMessage(text=message.get("text"),
                                 data={"elements": message.get("elements"),
                                       "buttons": message.get("buttons"),
                                       "attachment": message.get("image")})

        self.latest_bot_messages.append(bot_message)
        self.output_channel.send_response(self.sender_id, message)

    def line_template(self,
                      template: Text,
                      tracker: 'DialogueStateTracker',
                      silent_fail: bool = False,
                      **kwargs: Any
                      ) -> None:
        """"Send a message to the client based on a template."""

        message = self._generate_response(template,
                                          tracker,
                                          silent_fail,
                                          **kwargs)

        if not message:
            return

        self.line_response(message)
