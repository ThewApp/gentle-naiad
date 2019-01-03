from rasa_core.events import ReminderScheduled


class LineReminderScheduled(ReminderScheduled):
    def __init__(self, action_name, trigger_date_time, name=None,
                 kill_on_user_message=False, timestamp=None, data=None):
        self.data = data
        super().__init__(action_name, trigger_date_time,
                         name, kill_on_user_message, timestamp)
