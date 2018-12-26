import os
from rasa_core.agent import Agent


dirname = os.path.dirname(__file__)

def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="stories.md"):
    agent = Agent(os.path.join(dirname, domain_file))

    training_data = agent.load_data(os.path.join(dirname, training_data_file))
    agent.train(os.path.join(dirname, training_data))

    agent.persist(model_path)
    return agent

if __name__ == '__main__':
    train_dialogue()