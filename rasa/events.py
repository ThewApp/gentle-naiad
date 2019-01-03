from rasa_core.events import ReminderScheduled


class LineReminderScheduled(ReminderScheduled):
    def __init__(self, action_name, trigger_date_time, name=None,
                 kill_on_user_message=True, timestamp=None, data=None):
        """Creates the reminder
        Args:
            action_name: name of the action to be scheduled
            trigger_date_time: date at which the execution of the action
                should be triggered (either utc or with tz)
            name: id of the reminder. if there are multiple reminders with
                 the same id only the last will be run
            kill_on_user_message: ``True`` means a user message before the
                 trigger date will abort the reminder
            timestamp: creation date of the event
        """
        self.data = data
        super().__init__(action_name, trigger_date_time,
                         name, kill_on_user_message, timestamp)
