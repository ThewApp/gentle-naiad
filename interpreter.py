from rasa_core.interpreter import NaturalLanguageInterpreter

class LineEventInterpreter(NaturalLanguageInterpreter):
    def __init__(self, model_directory, config_file=None, lazy_init=False):
        self.model_directory = model_directory
        self.lazy_init = lazy_init
        self.config_file = config_file

        if not lazy_init:
            self._load_interpreter()
        else:
            self.interpreter = None

    def parse(self, event):
        """Parse an event object."""

        if self.lazy_init and self.interpreter is None:
            self._load_interpreter()
        parsed = self.interpreter.parse(event.message.text)
        parsed.event = event
        return parsed

    def _load_interpreter(self):
        from rasa_nlu.model import Interpreter

        self.interpreter = Interpreter.load(self.model_directory)