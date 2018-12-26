from rasa_core.agent import Agent


def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="stories.md"):
    agent = Agent(domain_file)

    training_data = agent.load_data(training_data_file)
    agent.train(training_data)

    agent.persist(model_path)
    return agent

if __name__ == '__main__':
    train_dialogue()