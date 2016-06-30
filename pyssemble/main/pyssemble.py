import logging
from argparse import ArgumentParser
from pprint import pprint

from pyssemble.config import Config
from pyssemble.python.python_sdist_creator import PythonSDistCreator

logging.basicConfig(level=logging.DEBUG)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("command", choices=["sdist", "config"])
    argument_parser.add_argument("--config", default="build.config")

    commandline_arguments = argument_parser.parse_args()

    config = Config(commandline_arguments.config)
    config.read()

    if commandline_arguments.command == "config":
        pprint(config.config, indent=2)

    if commandline_arguments.command == "sdist":
        sdist_creator = PythonSDistCreator(config)
        sdist_creator.create()


if __name__ == '__main__':
    main()
