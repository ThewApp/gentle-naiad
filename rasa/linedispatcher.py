from rasa_core.dispatcher import Dispatcher

from collections import namedtuple
from typing import Text, List, Optional, Callable, Any, Dict, Union

BotMessage = namedtuple("BotMessage", "text data")


class LineDispatcher(Dispatcher):
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

        self.utter_response(message)
