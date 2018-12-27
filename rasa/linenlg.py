import numpy as np
from rasa_core.nlg.generator import NaturalLanguageGenerator
from rasa_core.trackers import DialogueStateTracker

import copy
import logging
from typing import Text, Any, Dict, Optional, List

logger = logging.getLogger(__name__)


class LineNLG(NaturalLanguageGenerator):
    def __init__(self, domain):
        self.templates = domain.templates

    def _random_template_for(self, line_action: Text) -> Optional[Dict[Text, Any]]:
        """Select random template for the line action from available ones."""

        if line_action in self.templates:
            return np.random.choice(self.templates[line_action])
        else:
            return None

    def generate(self,
                 template_name: Text,
                 tracker: DialogueStateTracker,
                 output_channel: Text,
                 **kwargs: Any
                 ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        filled_slots = tracker.current_slot_values()
        return self.generate_from_slots(template_name,
                                        filled_slots,
                                        output_channel,
                                        **kwargs)

    def generate_from_slots(self,
                            template_name: Text,
                            filled_slots: Dict[Text, Any],
                            output_channel: Text,
                            **kwargs: Any
                            ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        # Fetching a random template for the passed template name
        r = copy.deepcopy(self._random_template_for(template_name))
        # Filling the slots in the template and returning the template
        print(r)
        if r is not None:
            return self._fill_template_text(r, filled_slots, **kwargs)
        else:
            return None

    def _fill_template_text(
        self,
        template: Dict[Text, Any],
        filled_slots: Optional[Dict[Text, Any]] = None,
        **kwargs: Any
    ) -> Dict[Text, Any]:
        """"Combine slot values and key word arguments to fill templates."""

        # Getting the slot values in the template variables
        template_vars = self._template_variables(filled_slots, kwargs)

        # Filling the template variables in the template
        if template_vars:
            try:
                if type(template) == list:
                    for item in template:
                        if "text" in item:
                            item["text"] = item["text"].format(**template_vars)
                else:
                    template["text"] = template["text"].format(**template_vars)
            except KeyError as e:
                logger.exception(
                    "Failed to fill line template '{}'. "
                    "Tried to replace '{}' but could not find "
                    "a value for it. There is no slot with this "
                    "name nor did you pass the value explicitly "
                    "when calling the template. Return template "
                    "without filling the template. "
                    "".format(template, e.args[0]))
        return template

    @staticmethod
    def _combine_template_variables(filled_slots: Dict[Text, Any],
                                    kwargs: Dict[Text, Any]) -> Dict[Text, Any]:
        """Combine slot values and key word arguments to fill templates."""

        if filled_slots is None:
            filled_slots = {}

        # Copying the filled slots in the template variables.
        template_vars = filled_slots.copy()
        template_vars.update(kwargs)
        return template_vars
