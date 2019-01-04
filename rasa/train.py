import argparse


def train_core():
    from rasa.lineagent import LineAgent
    from rasa_core import config
    import os
    policy_config = os.path.join(os.path.dirname(
        config.__file__), "default_config.yml")
    policies = config.load(policy_config)
    agent = LineAgent("domain.yml", policies=policies)
    data = agent.load_data("stories.md")
    agent.train(data)
    agent.persist("models/dialogue")
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer
    training_data = load_data('nlu.md')
    trainer = Trainer(config.load("nlu_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")
    return model_directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['core', 'nlu'])
    args = parser.parse_args()
    if args.type == "core":
        train_core()
    elif args.type == "nlu":
        train_nlu()
