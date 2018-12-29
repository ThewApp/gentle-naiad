from collections import namedtuple
from typing import Any, Callable, Dict, List, Optional, Text, Union

from rasa_core.dispatcher import Dispatcher

BotMessage = namedtuple("BotMessage", "text data")


class LineDispatcher(Dispatcher):
    def line_response(self, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""

        if hasattr(self.output_channel, "add_reply"):
            self.output_channel.add_reply(self.sender_id, message)
        else:
            import json
            self.output_channel.send_response(
                self.sender_id, {'text': json.dumps(message, sort_keys=True, indent=2, ensure_ascii=False)})

    def line_template(self,
                      template: Text,
                      tracker: 'DialogueStateTracker',
                      **kwargs: Any
                      ) -> None:
        """"Send a message to the client based on a template."""

        message = self.nlg.generate(template, tracker, **kwargs)

        if not message:
            return

        if type(message) == list:
            for item in message:
                self.line_response(item)
        else:
            self.line_response(message)
