from rasa_core.actions.action import (
    UtterAction, RemoteAction,
    ACTION_DEFAULT_FALLBACK_NAME, ACTION_RESTART_NAME,
    Action, ActionListen, ActionDeactivateForm
)
from rasa_core.utils import EndpointConfig
import rasa.actions

import logging
from typing import Text, List, Optional, Callable, Any, Dict, Union

logger = logging.getLogger(__name__)


def default_actions() -> List['Action']:
    """List default actions."""
    return [ActionListen(), ActionRestart(),
            ActionDefaultFallback(), ActionDeactivateForm()]


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
    elif name.startswith("custom_"):
        return get_custom_action(name)
    else:
        return RemoteAction(name, action_endpoint)


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return ACTION_DEFAULT_FALLBACK_NAME

    def run(self, dispatcher, tracker, domain):
        from rasa_core.events import UserUtteranceReverted

        dispatcher.line_template("line_default", tracker)

        return [UserUtteranceReverted()]


class ActionRestart(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return ACTION_RESTART_NAME

    def run(self, dispatcher, tracker, domain):
        from rasa_core.events import Restarted

        return [Restarted()]


class LineAction(Action):
    def __init__(self, name):
        self._name = name

    def run(self, dispatcher, tracker, domain):
        dispatcher.line_template(self.name(), tracker)
        return []

    def name(self) -> Text:
        return self._name

    def __str__(self) -> Text:
        return "LineAction('{}')".format(self.name())


def get_custom_action(name):
    try:
        action = getattr(rasa.actions, name)
        return action()
    except AttributeError:
        logger.error("%s action not found in %s", name, rasa.actions.__name__)
        return ActionDefaultFallback()
