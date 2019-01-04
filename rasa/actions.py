from datetime import datetime, timedelta
import logging

from rasa_core.actions.action import Action
from rasa_core.constants import REQUESTED_SLOT
from rasa_core.events import SlotSet, Form, FollowupAction
from rasa.linedispatcher import LineDispatcher

from rasa.constants import DEFAULT_REMINDER
from rasa.events import LineReminderScheduled
from rasa.lineform import LineForm
from rasa.template.flex_medicine_list import get_flex_medicine_list

logger = logging.getLogger(__name__)


class custom_form_add_medicine(LineForm):
    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "custom_form_add_medicine"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        require_meal_times = [
            "morning", "noon", "evening"
        ]

        new_medicine_time = tracker.get_slot("new_medicine_time")

        if (new_medicine_time and
            not any(require_meal_time in new_medicine_time
            for require_meal_time in require_meal_times)):
            return ["new_medicine_name", "new_medicine_time"]

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
            "new_medicine_time": self.from_entity(intent="enter_medicine_data", entity="time"),
            "new_medicine_meal": self.from_entity(intent="enter_medicine_data", entity="meal")
        }

    def submit(self, dispatcher: LineDispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""

        medicine_list = tracker.get_slot("medicine_list")

        if medicine_list is None:
            new_medicine_list = []
        else:
            new_medicine_list = medicine_list.copy()

        new_medicine_name = tracker.get_slot("new_medicine_name")
        new_medicine_time = tracker.get_slot("new_medicine_time")
        new_medicine_meal = tracker.get_slot("new_medicine_meal")

        new_medicine_list.append({
            "name": new_medicine_name,
            "time": new_medicine_time,
            "meal": new_medicine_meal
        })

        # utter submit template
        dispatcher.line_template('line_add_new_medicine_success', tracker)

        events = [
            SlotSet("medicine_list", new_medicine_list),
            SlotSet("new_medicine_name", None),
            SlotSet("new_medicine_time", None),
            SlotSet("new_medicine_meal", None),
            FollowupAction("custom_medicine_reminder_update")
        ]

        return events


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

        return [SlotSet("medicine_list", new_medicine_list), FollowupAction("custom_medicine_reminder_update")]


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

        medicine_list = tracker.get_slot("medicine_list")
        if medicine_list:
            first_medicine = medicine_list[0]
            time = first_medicine["time"].split("_")[0]
            meal = first_medicine["meal"]
        else:
            return []
        schedule_time = datetime.utcnow() + timedelta(seconds=10)
        reminder = LineReminderScheduled("custom_medicine_reminder_push",
                                         schedule_time,
                                         data={
                                             "time_tuple": (time, meal)
                                         })

        dispatcher.line_template("line_test_reminder_setup", tracker)

        return [reminder]


class custom_medicine_reminder_update(Action):
    def name(self):
        # type: () -> Text
        return "custom_medicine_reminder_update"

    def run(self, dispatcher: LineDispatcher, tracker, domain):
        medicine_list = tracker.get_slot("medicine_list")
        medicine_reminders = tracker.get_slot("medicine_reminders")
        events = []

        if medicine_reminders is None:
            medicine_reminders = DEFAULT_REMINDER

        checked = []

        for medicine in medicine_list:
            medicine_time = medicine["time"]
            times = medicine_time.split("_")
            meal = medicine["meal"]
            for time in times:
                if (time, meal) in medicine_reminders and (time, meal) not in checked:
                    checked.append((time, meal))
                    if medicine_reminders[(time, meal)]["job_id"] is None:
                        reminder = self.generateScheduled(
                            medicine_reminders, (time, meal))
                        logger.debug(
                            "Adding reminder... time:{}".format(reminder))
                        events.append(reminder)

        for reminder in medicine_reminders:
            if reminder in checked:
                continue
            elif medicine_reminders[reminder]["job_id"] is not None:
                cancel_reminder = self.cancelScheduled(
                    medicine_reminders, reminder)
                logger.debug(
                    "Canceling reminder... time:{}".format(reminder))
                events.append(cancel_reminder)

        return events

    @staticmethod
    def generateScheduled(medicine_reminders, time_tuple):
        reminder_info = medicine_reminders[time_tuple]
        time = reminder_info["time"]
        utcnow = datetime.utcnow()
        schedule_time = datetime.combine(utcnow, time)
        if utcnow > schedule_time:
            schedule_time = schedule_time + timedelta(days=1)
        reminder = LineReminderScheduled("custom_medicine_reminder_push",
                                         schedule_time,
                                         data={
                                             "time_tuple": time_tuple
                                         })
        return reminder

    @staticmethod
    def cancelScheduled(medicine_reminders, time_tuple):
        name = medicine_reminders[time_tuple]["job_id"]
        reminder = LineReminderScheduled("custom_medicine_reminder_push",
                                         None,
                                         name=name,
                                         cancel=True)
        return reminder


class custom_medicine_reminder_push(Action):
    def name(self):
        # type: () -> Text
        return "custom_medicine_reminder_push"

    def run(self, dispatcher: LineDispatcher, tracker, domain):
        medicine_list = tracker.get_slot("medicine_list")
        medicine_reminders = tracker.get_slot("medicine_reminders")
        time_tuple = dispatcher.reminder_data.get("time_tuple")
        
        if medicine_list and time_tuple:
            medicine_to_remind = []
            time_text = medicine_reminders[time_tuple]["time_text"]
            if time_tuple[1]:
                meal_text = " " + medicine_reminders[time_tuple]["meal_text"]
            else:
                meal_text = ""
            for medicine in medicine_list:
                time = medicine["time"]
                meal = medicine["meal"]
                if (time, meal) == time_tuple:
                    medicine_to_remind.append(medicine["name"])
            
            number_to_remind = len(medicine_to_remind)
            if number_to_remind > 0:
                if number_to_remind == 1:
                    text = "สวัสดีค่ะ คุณทาน{} ตอน{}{} หรือยังคะ".format(
                        medicine_to_remind[0], time_text, meal_text)
                else:
                    text = "สวัสดีค่ะ คุณทาน\n"
                    for medicine in medicine_to_remind:
                        text += "❥ " + medicine + "\n"
                    text += "ตอน{}{} หรือยังคะ".format(
                        time_text, meal_text)
                dispatcher.line_template(
                    "line_medicine_reminder_push", tracker, text=text)
            medicine_reminders[time_tuple]["job_id"] = None

            return [SlotSet("medicine_reminders", medicine_reminders), FollowupAction("custom_medicine_reminder_update")]

        return []
