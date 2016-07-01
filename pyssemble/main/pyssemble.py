import logging
import os
from argparse import ArgumentParser
from pprint import pprint

from pyssemble.config.config_reader import ConfigReader
from pyssemble.python.python_sdist_creator import PythonSDistCreator

logging.basicConfig(level=logging.DEBUG)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("command", choices=["sdist", "config"])

    commandline_arguments = argument_parser.parse_args()

    config_reader = ConfigReader(os.getcwd())
    config = config_reader.read()

    if commandline_arguments.command == "config":
        pprint(config, indent=2)

    if commandline_arguments.command == "sdist":
        sdist_creator = PythonSDistCreator(config)
        sdist_creator.create()


if __name__ == '__main__':
    main()
