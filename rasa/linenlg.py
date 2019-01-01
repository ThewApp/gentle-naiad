from rasa_core.nlg.generator import NaturalLanguageGenerator
from rasa_core.trackers import DialogueStateTracker

import copy
import logging
import random
from typing import Text, Any, Dict, Optional, List

logger = logging.getLogger(__name__)


class LineNLG(NaturalLanguageGenerator):
    def __init__(self, domain):
        self.templates = domain.templates

    def _random_template_for(self, line_action: Text) -> Optional[Dict[Text, Any]]:
        """Select random template for the line action from available ones."""

        if line_action in self.templates:
            return random.choice(self.templates[line_action])
        else:
            return None

    def generate(self,
                 template_name: Text,
                 tracker: DialogueStateTracker,
                 **kwargs: Any
                 ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        filled_slots = tracker.current_slot_values()
        return self.generate_from_slots(template_name,
                                        filled_slots,
                                        **kwargs)

    def generate_from_slots(self,
                            template_name: Text,
                            filled_slots: Dict[Text, Any],
                            **kwargs: Any
                            ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        # Fetching a random template for the passed template name
        r = copy.deepcopy(self._random_template_for(template_name))
        # Filling the slots in the template and returning the template
        if r is not None:
            # Getting the slot values in the template variables
            template_vars = self._combine_template_variables(filled_slots, kwargs)
            
            return self._fill_template(r, template_vars)
        else:
            return None

    def _fill_template_text(
        self,
        template: Dict[Text, Any],
        template_vars: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """"Combine slot values and key word arguments to fill templates."""
        line_text_keys = ["text", "altText", "label"]
        try:
            for key in line_text_keys:
                if key in template:
                    template[key] = template[key].format(**template_vars)
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


    def _fill_template(
        self,
        template: Dict[Text, Any],
        template_vars: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """"Fill text in template"""

        line_object_keys = ["quickReply", "items", "action", "template", "actions"]

        if type(template) == list:
            for item in template:
                self._fill_template(item, template_vars)
        else:
            self._fill_template_text(template, template_vars)
            for key in line_object_keys:
                if key in template:
                    self._fill_template(template[key], template_vars)

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
