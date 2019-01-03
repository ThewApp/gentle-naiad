from rasa_core.agent import Agent
from rasa_core.channels.channel import UserMessage
from rasa_core.events import Event, ReminderScheduled, UserUttered
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.policies import Policy
from rasa_core.policies.ensemble import PolicyEnsemble
from rasa_core.processor import MessageProcessor
from rasa_core.utils import EndpointConfig
from rasa.linedispatcher import LineDispatcher
from rasa.linedomain import LineDomain
from rasa.linenlg import LineNLG
from rasa.store import scheduler_store
from rq_scheduler import Scheduler

import logging
import os
from typing import Text, List, Optional, Callable, Any, Dict, Union

logger = logging.getLogger(__name__)

if scheduler_store:
    scheduler = Scheduler(connection=scheduler_store)


class LineAgent(Agent):
    def __init__(
        self,
        domain: Union[Text, LineDomain] = None,
        policies: Union[PolicyEnsemble, List[Policy], None] = None,
        interpreter: Optional[NaturalLanguageInterpreter] = None,
        generator: Union[EndpointConfig, 'NLG', None] = None,
        tracker_store: Optional['TrackerStore'] = None,
        action_endpoint: Optional[EndpointConfig] = None,
        fingerprint: Optional[Text] = None
    ):
        super().__init__(domain, policies, interpreter, generator,
                         tracker_store, action_endpoint, fingerprint)
        self.nlg = LineNLG(self.domain)

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

    def handle_reminder(self,
                        reminder_event: ReminderScheduled,
                        dispatcher: LineDispatcher
                        ) -> None:
        """Handle a reminder that is triggered asynchronously."""

        tracker = self._get_tracker(dispatcher.sender_id)

        if not tracker:
            logger.warning("Failed to retrieve or create tracker for sender "
                           "'{}'.".format(dispatcher.sender_id))
            return None

        if (reminder_event.kill_on_user_message and
                self._has_message_after_reminder(tracker, reminder_event) or not
                self._is_reminder_still_valid(tracker, reminder_event)):
            logger.debug("Canceled reminder because it is outdated. "
                         "(event: {} id: {})".format(reminder_event.action_name,
                                                     reminder_event.name))
        else:
            # necessary for proper featurization, otherwise the previous
            # unrelated message would influence featurization
            tracker.update(UserUttered.empty())
            action = self._get_action(reminder_event.action_name)
            should_continue = self._run_action(action, tracker, dispatcher)
            dispatcher.output_channel.send_push()
            if should_continue:
                user_msg = UserMessage(None,
                                       dispatcher.output_channel,
                                       dispatcher.sender_id)
                self._predict_and_execute_next_action(user_msg, tracker)
            # save tracker state to continue conversation from this state
            self._save_tracker(tracker)

    @classmethod
    def handle_reminder_worker(cls, e, dispatcher):
        logger.debug("Event name: %s", e.name)

    def _schedule_reminders(self, events: List[Event],
                            dispatcher: LineDispatcher) -> None:
        """Uses the scheduler to time a job to trigger the passed reminder.
        Reminders with the same `id` property will overwrite one another
        (i.e. only one of them will eventually run)."""

        if events is not None:
            for e in events:
                if isinstance(e, ReminderScheduled):
                    scheduler.enqueue_at(
                        e.trigger_date_time,
                        LineMessageProcessor.handle_reminder_worker,
                        e,
                        dispatcher,
                        job_id=e.name
                    )
