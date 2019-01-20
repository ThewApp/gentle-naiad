from rasa_core.actions import Action
from rasa_core.domain import Domain
from rasa_core.utils import EndpointConfig
from rasa.lineaction import action_from_name

from typing import Text, List, Optional, Callable, Any, Dict, Union


class LineDomain(Domain):
    def action_for_name(self,
                        action_name: Text,
                        action_endpoint: Optional[EndpointConfig]
                        ) -> Optional[Action]:
        """Looks up which action corresponds to this action name."""

        if action_name not in self.action_names:
            self._raise_action_not_found_exception(action_name)

        return action_from_name(action_name,
                                action_endpoint,
                                self.user_actions_and_forms)

    @staticmethod
    def collect_templates(
        yml_templates: Dict[Text, List[Any]]
    ) -> Dict[Text, List[Dict[Text, Any]]]:
        """Go through the templates and make sure they are all in dict format
        """
        templates = {}
        for template_key, template_variations in yml_templates.items():
            isLine = template_key.startswith("line_")
            validated_variations = []
            for t in template_variations:
                # templates can either directly be strings or a dict with
                # options we will always create a dict out of them
                if isinstance(t, str) and not isLine:
                    validated_variations.append({"text": t})
                elif isLine and isinstance(t, dict) and "type" not in t:
                    raise SyntaxError(f"template: {template_key} must has `type` property")
                elif isLine and isinstance(t, list):
                    for index, message in enumerate(t):
                        if "type" not in message:
                            raise SyntaxError(f"template: \"{template_key}\" message index: \"{index}\" must has `type` property")
                else:
                    validated_variations.append(t)
            templates[template_key] = validated_variations
        return templates
