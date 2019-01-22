import argparse
import logging

import coloredlogs


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
    model_directory = trainer.persist('models/',
                                      project_name="current",
                                      fixed_model_name="nlu")
    return model_directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode',
        help="Selecting training mode",
        choices=['core', 'nlu']
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose. Sets logging level to INFO",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.INFO,
    )
    parser.add_argument(
        '-vv', '--debug',
        help="Print lots of debugging statements. "
                "Sets logging level to DEBUG",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    parser.add_argument(
        '--quiet',
        help="Be quiet! Sets logging level to WARNING",
        action="store_const",
        dest="loglevel",
        const=logging.WARNING,
    )
    args = parser.parse_args()
    coloredlogs.install(level=args.loglevel)
    if args.mode == "core":
        train_core()
    elif args.mode == "nlu":
        train_nlu()
