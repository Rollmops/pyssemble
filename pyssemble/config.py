import collections
import json
import logging
import os
import sys

from pyssemble.dotted_template import DottedTemplate

LOGGER = logging.getLogger(__name__)


class Config:
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
        self.build_config_dir = os.path.dirname(self.path)
        self.config = {}

    def __getitem__(self, item):
        config_entry_file_path = os.path.join(self.build_config_dir, item)
        if item in self.config:
            if os.path.exists(config_entry_file_path):
                LOGGER.warning("Found config entry '%s' in '%s' and in file '%s'. Using the entry from '%s'" % (
                    item, self.path, config_entry_file_path, self.path))
            return self.config[item]

        if os.path.exists(config_entry_file_path):
            with open(config_entry_file_path) as config_entry_file_pointer:
                return config_entry_file_pointer.read()

    def keys(self):
        return self.config.keys()

    def read(self):
        if not os.path.exists(self.path):
            LOGGER.error("Unable to find '%s'" % (self.path))
            sys.exit(-1)

        with open(self.path) as config_file_pointer:
            self.config = Config._flatten(json.load(config_file_pointer))

        self._set_default_for_missing()
        self._set_references()
        self._check()

    def _check(self):
        for key, value in self.config.items():
            config_entry_file_path = os.path.join(self.build_config_dir, key)
            if key in self.config:
                if os.path.exists(config_entry_file_path):
                    LOGGER.warning("Found config entry '%s' in '%s' and in file '%s'. Using the entry from '%s'" % (
                        key, self.path, config_entry_file_path, self.path))

    def _set_references(self):
        for key, value in self.config.items():
            value_template = DottedTemplate(str(value))
            value = value_template.substitute(self.config)
            self.config[key] = value

    def _set_default_for_missing(self):
        for key, value in Config.DEFAULT_VALUES.items():
            if not key in self.config:
                self.config[key] = value

    @staticmethod
    def _flatten(dictionary, parent_key="", sep="."):
        items = []
        for k, v in dictionary.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(Config._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
