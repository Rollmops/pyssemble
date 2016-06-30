import collections
import json
import logging
import os

from pyssemble.common.recursive_path_iterate import recursive_path_iterate
from pyssemble.dotted_template import DottedTemplate

LOGGER = logging.getLogger(__name__)


class ConfigReader:
    DEFAULT_VALUES = {
        "project.build_path": os.path.join(os.getcwd(), "build"),
        "project.author": os.environ.get("PROJECT_AUTHOR", "UNKNOWN"),
        "project.author_email": os.environ.get("PROJECT_AUTHOR_EMAIL", "UNKNOWN"),
        "project.url": os.environ.get("PROJECT_URL", "UNKNOWN"),
        "packaging.prefix": "/usr/local",
        "packaging.prefix_main": "${packaging.prefix}/bin",
        "packaging.prefix_lib": "${packaging.prefix}/lib",
    }

    def __init__(self, path):
        self.path = path

    def read(self):
        if not os.path.exists(self.path):
            raise ConfigReader.NoBuildConfigError("Unable to find '%s'" % (self.path))

        with open(self.path) as config_file_pointer:
            config = ConfigReader._flatten(json.load(config_file_pointer))

        self._set_default_for_missing(config)
        self._add_config_from_config_dir(config)
        self._set_references(config)

        return config

    def _add_config_from_config_dir(self, config):
        additional_config_dir = os.path.join(os.path.dirname(self.path), "config")
        if os.path.isdir(additional_config_dir):
            for path in recursive_path_iterate(additional_config_dir, "*"):
                config_path = path[len(additional_config_dir):]
                config_path = ".".join(config_path.split("/")).strip(".")

                if not config_path in config:
                    LOGGER.debug("Using config '%s' from '%s'" % (config_path, path))
                    with open(path) as config_file_pointer:
                        config[config_path] = config_file_pointer.read().strip()
                else:
                    raise ConfigReader.DuplicateConfigItemError(
                        "Found duplicate config item '%s' in '%s' and '%s'" % (config_path, self.path, path))

    @staticmethod
    def _set_references(config):
        for key, value in config.items():
            value_template = DottedTemplate(str(value))
            value = value_template.substitute(config)
            config[key] = value

    @staticmethod
    def _set_default_for_missing(config):
        for key, value in ConfigReader.DEFAULT_VALUES.items():
            if not key in config:
                config[key] = value

    @staticmethod
    def _flatten(dictionary, parent_key="", sep="."):
        items = []
        for k, v in dictionary.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(ConfigReader._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    class DuplicateConfigItemError(RuntimeError):
        pass

    class NoBuildConfigError(RuntimeError):
        pass
