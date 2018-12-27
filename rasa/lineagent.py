from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.policies.ensemble import PolicyEnsemble
from rasa_core.processor import MessageProcessor
from rasa_core.utils import EndpointConfig
from rasa.linedispatcher import LineDispatcher
from rasa.linedomain import LineDomain

import logging
import os
from typing import Text, List, Optional, Callable, Any, Dict, Union

logger = logging.getLogger(__name__)


class LineAgent(Agent):
    def create_processor(self,
                         preprocessor: Optional[Callable[[Text], Text]] = None
                         ) -> MessageProcessor:
        """Instantiates a processor based on the set state of the agent."""
        # Checks that the interpreter and tracker store are set and
        # creates a processor
        self._ensure_agent_is_ready()
        return LineMessageProcessor(
            self.interpreter,
            self.policy_ensemble,
            self.domain,
            self.tracker_store,
            self.nlg,
            action_endpoint=self.action_endpoint,
            message_preprocessor=preprocessor)

    @classmethod
    def load(cls,
             path: Text,
             interpreter: Optional[NaturalLanguageInterpreter] = None,
             generator: Union[EndpointConfig, 'NLG'] = None,
             tracker_store: Optional['TrackerStore'] = None,
             action_endpoint: Optional[EndpointConfig] = None,
             ) -> 'Agent':
        """Load a persisted model from the passed path."""

        if not path:
            raise ValueError("You need to provide a valid directory where "
                             "to load the agent from when calling "
                             "`Agent.load`.")

        if os.path.isfile(path):
            raise ValueError("You are trying to load a MODEL from a file "
                             "('{}'), which is not possible. \n"
                             "The persisted path should be a directory "
                             "containing the various model files. \n\n"
                             "If you want to load training data instead of "
                             "a model, use `agent.load_data(...)` "
                             "instead.".format(path))

        domain = LineDomain.load(os.path.join(path, "domain.yml"))
        ensemble = PolicyEnsemble.load(path) if path else None

        # ensures the domain hasn't changed between test and train
        domain.compare_with_specification(path)

        return cls(domain=domain,
                   policies=ensemble,
                   interpreter=interpreter,
                   generator=generator,
                   tracker_store=tracker_store,
                   action_endpoint=action_endpoint)

    @staticmethod
    def _create_domain(domain: Union[None, LineDomain, Text]) -> LineDomain:

        if isinstance(domain, str):
            return LineDomain.load(domain)
        elif isinstance(domain, LineDomain):
            return domain
        elif domain is not None:
            raise ValueError(
                "Invalid param `domain`. Expected a path to a domain "
                "specification or a domain instance. But got "
                "type '{}' with value '{}'".format(type(domain), domain))


class LineMessageProcessor(MessageProcessor):
    def _predict_and_execute_next_action(self, message, tracker):
        # this will actually send the response to the user

        dispatcher = LineDispatcher(message.sender_id,
                                    message.output_channel,
                                    self.nlg)
        # keep taking actions decided by the policy until it chooses to 'listen'
        should_predict_another_action = True
        num_predicted_actions = 0

        self._log_slots(tracker)

        # action loop. predicts actions until we hit action listen
        while (should_predict_another_action and
               self._should_handle_message(tracker) and
               num_predicted_actions < self.max_number_of_predictions):
            # this actually just calls the policy's method by the same name
            action, policy, confidence = self.predict_next_action(tracker)

            should_predict_another_action = self._run_action(action,
                                                             tracker,
                                                             dispatcher,
                                                             policy,
                                                             confidence)
            num_predicted_actions += 1

        if (num_predicted_actions == self.max_number_of_predictions and
                should_predict_another_action):
            # circuit breaker was tripped
            logger.warning(
                "Circuit breaker tripped. Stopped predicting "
                "more actions for sender '{}'".format(tracker.sender_id))
            if self.on_circuit_break:
                # call a registered callback
                self.on_circuit_break(tracker, dispatcher)
