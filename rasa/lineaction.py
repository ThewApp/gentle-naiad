from rasa_core.actions.action import UtterAction, RemoteAction, default_actions, Action
from rasa_core.utils import EndpointConfig

from typing import Text, List, Optional, Callable, Any, Dict, Union


def action_from_name(name: Text, action_endpoint: Optional[EndpointConfig],
                     user_actions: List[Text]) -> 'Action':
    """Return an action instance for the name."""

    defaults = {a.name(): a for a in default_actions()}

    if name in defaults and name not in user_actions:
        return defaults.get(name)
    elif name.startswith("utter_"):
        return UtterAction(name)
    elif name.startswith("line_"):
        return LineAction(name)
    else:
        return RemoteAction(name, action_endpoint)


class LineAction(Action):

    def __init__(self, name):
        self._name = name

    def run(self, dispatcher, tracker, domain):
        """Simple run implementation uttering a (hopefully defined) template."""

        dispatcher.line_template(self.name(),
                                  tracker)
        return []

    def name(self) -> Text:
        return self._name

    def __str__(self) -> Text:
        return "LineAction('{}')".format(self.name())
