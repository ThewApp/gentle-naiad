from rasa.lineagent import LineAgent
from rasa_core import config
import os

if __name__ == "__main__":
    policy_config = os.path.join(os.path.dirname(config.__file__), "default_config.yml")
    policies = config.load(policy_config)
    agent = LineAgent("domain.yml", policies=policies)
    data = agent.load_data("stories.md")
    agent.train(data)
    agent.persist("models/dialogue")