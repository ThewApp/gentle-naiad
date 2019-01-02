from datetime import datetime, timedelta

from rasa_core.actions.action import Action
from rasa_core.constants import REQUESTED_SLOT
from rasa_core.events import SlotSet, Form, ReminderScheduled
from rasa.linedispatcher import LineDispatcher

from rasa.lineform import LineForm
from rasa.template.flex_medicine_list import get_flex_medicine_list


class custom_form_add_medicine(LineForm):
    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "custom_form_add_medicine"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        return ["new_medicine_name", "new_medicine_time", "new_medicine_meal"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Text, Dict, List[Text, Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked"""

        return {
            "new_medicine_name": self.from_text(not_intent="negative"),
            "new_medicine_time": self.from_text(intent="enter_medicine_data"),
            "new_medicine_meal": self.from_text(intent="enter_medicine_data")
        }

    def submit(self, dispatcher: LineDispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""

        medicine_list = tracker.get_slot("medicine_list")
        if medicine_list is None:
            new_medicine_list = []
        else:
            new_medicine_list = medicine_list.copy()

        new_medicine_list.append({
            "name": tracker.get_slot("new_medicine_name"),
            "time": tracker.get_slot("new_medicine_time"),
            "meal": tracker.get_slot("new_medicine_meal")
        })

        # utter submit template
        dispatcher.line_template('line_add_new_medicine_success', tracker)
        return [
            SlotSet("medicine_list", new_medicine_list),
            SlotSet("new_medicine_name", None),
            SlotSet("new_medicine_time", None),
            SlotSet("new_medicine_meal", None)
        ]


class custom_reset_add_new_medicine(Action):
    def name(self):
        # type: () -> Text
        return "custom_reset_add_new_medicine"

    def run(self, dispatcher: LineDispatcher, tracker, domain):

        dispatcher.line_template('line_cancel_success', tracker)

        return [
            Form(None),
            SlotSet("new_medicine_name", None),
            SlotSet("new_medicine_time", None),
            SlotSet("new_medicine_meal", None),
            SlotSet(REQUESTED_SLOT, None)
        ]


class custom_remove_medicine(Action):
    def name(self):
        # type: () -> Text
        return "custom_remove_medicine"

    def run(self, dispatcher: LineDispatcher, tracker, domain):

        new_medicine_list = tracker.get_slot("medicine_list").copy()

        index = next(tracker.get_latest_entity_values(
            "remove_medicine_index"), None)

        removed_medicine = new_medicine_list.pop(index)

        dispatcher.line_template(
            'line_remove_medicine_success', tracker, medicine_name=removed_medicine["name"])

        return [SlotSet("medicine_list", new_medicine_list)]


class custom_flex_medicine_list(Action):
    def name(self):
        # type: () -> Text
        return "custom_flex_medicine_list"

    def run(self, dispatcher: LineDispatcher, tracker, domain):

        medicine_list = tracker.get_slot("medicine_list")

        message = get_flex_medicine_list(medicine_list)

        dispatcher.line_response(message)

        return []


class custom_test_reminder_setup(Action):
    def name(self):
        # type: () -> Text
        return "custom_test_reminder_setup"

    def run(self, dispatcher: LineDispatcher, tracker, domain):

        dispatcher.line_template("line_test_reminder_setup", tracker)

        return [ReminderScheduled("line_medicine_reminder_push", datetime.utcnow() + timedelta(seconds=10))]
