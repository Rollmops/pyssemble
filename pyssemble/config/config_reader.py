import logging
import os
from glob import glob

from pyssemble.config.common import MultipleBuildConfigFilesError, NoBuildConfigFileError
from pyssemble.config.json_config_reader_strategy import JSONConfigReaderStrategy
from pyssemble.dotted_template import DottedTemplate

LOGGER = logging.getLogger(__name__)


class ConfigReader:
    DEFAULT_VALUES = {
        "project.author": os.environ.get("PROJECT_AUTHOR", "UNKNOWN"),
        "project.author_email": os.environ.get("PROJECT_AUTHOR_EMAIL", "UNKNOWN"),
        "project.url": os.environ.get("PROJECT_URL", "UNKNOWN"),
        "packaging.prefix": "/usr/local",
        "build_path": os.path.join(os.getcwd(), "build"),
    }

    def __init__(self, root_path):
        self.root_path = root_path

    def read(self):
        config_file_path = self._find_build_config_file()

        chain_entry = self._setup_responsibility_chain()

        config = chain_entry.read(config_file_path)

        self._set_default_for_missing(config)
        self._set_references(config)

        config["root_path"] = self.root_path

        return config

    def _find_build_config_file(self):
        config_file_path_list = glob(os.path.join(self.root_path, "build.*"))
        if len(config_file_path_list) > 1:
            raise MultipleBuildConfigFilesError(
                "Found multiple build config files: '%s'" % config_file_path_list)
        if len(config_file_path_list) == 0:
            raise NoBuildConfigFileError("Unable to find build config file in '%s'" % self.root_path)
        return config_file_path_list[0]

    @staticmethod
    def _setup_responsibility_chain():
        json_config_reader_strategy = JSONConfigReaderStrategy()
        return json_config_reader_strategy

    @staticmethod
    def _set_references(config):
        for key, value in config.items():
            if isinstance(value, str):
                value_template = DottedTemplate(value)
                value = value_template.substitute(config)
                config[key] = value

    @staticmethod
    def _set_default_for_missing(config):
        for key, value in ConfigReader.DEFAULT_VALUES.items():
            if not key in config:
                config[key] = value
