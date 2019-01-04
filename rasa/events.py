from rasa_core.events import Event, ReminderScheduled


class LineReminderScheduled(ReminderScheduled):
    type_name = "line_reminder"

    def __init__(self, action_name, trigger_date_time, name=None,
                 kill_on_user_message=False, data=None, cancel=False, timestamp=None):
        self.data = data
        self.cancel = cancel
        super().__init__(action_name, trigger_date_time,
                         name, kill_on_user_message, timestamp)
