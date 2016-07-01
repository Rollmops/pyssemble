import json

from pyssemble.config.common import flatten, NoConfigReaderStrategyError


class JSONConfigReaderStrategy:
    def __init__(self, next_strategy=None):
        self.next_strategy = next_strategy

    def read(self, config_file_path):
        if not config_file_path.endswith(".json"):
            if not self.next_strategy:
                raise NoConfigReaderStrategyError(
                    "No config reader strategy for file '%s'" % config_file_path)
            return self.next_strategy.read(config_file_path)

        return JSONConfigReaderStrategy._read(config_file_path)

    @staticmethod
    def _read(config_file_path):
        with open(config_file_path) as fp:
            config_as_dict = json.load(fp)

        flattened_config = flatten(config_as_dict)

        return flattened_config
