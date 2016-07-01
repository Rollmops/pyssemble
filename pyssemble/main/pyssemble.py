import logging
import os
from argparse import ArgumentParser
from pprint import pprint

from pyssemble.config.config_reader import ConfigReader
from pyssemble.plugin_loader import PluginLoader
from pyssemble.runner import Runner

logging.basicConfig(level=logging.DEBUG)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--show-config", action="store_true", help="Show all config parameters")
    argument_parser.add_argument("--no-base-plugins", action="store_true")

    commandline_arguments, phases = argument_parser.parse_known_args()

    config_reader = ConfigReader(os.getcwd())
    config = config_reader.read()

    plugin_loader = PluginLoader()
    runner = Runner(config, plugin_loader)
    runner.init(load_base_plugins=not commandline_arguments.no_base_plugins)

    if commandline_arguments.show_config:
        pprint(config, indent=2)

    for phase in phases:
        runner.run_phase(phase)


if __name__ == '__main__':
    main()
