import logging
import os
from argparse import ArgumentParser
from pprint import pprint

from pyssemble.config_reader import ConfigReader
from pyssemble.python.python_sdist_creator import PythonSDistCreator

logging.basicConfig(level=logging.DEBUG)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("command", choices=["sdist", "config"])
    argument_parser.add_argument("--config", default=os.path.join(os.getcwd(), "build.config"))

    commandline_arguments = argument_parser.parse_args()

    config_reader = ConfigReader(commandline_arguments.config)
    config = config_reader.read()

    if commandline_arguments.command == "config":
        pprint(config, indent=2)

    if commandline_arguments.command == "sdist":
        sdist_creator = PythonSDistCreator(config)
        sdist_creator.create()


if __name__ == '__main__':
    main()
