import logging

from pyssemble.common.recursive_path_iterate import recursive_path_iterate
from pyssemble.dotted_template import DottedTemplate

LOGGER = logging.getLogger(__name__)


class ResourceInjector:
    def __init__(self, path, config):
        self.path = path
        self.config = config

    def inject(self):
        for file in recursive_path_iterate(self.path, "*"):
            with open(file) as file_pointer:
                content = file_pointer.read()
            template = DottedTemplate(content)
            with open(file, "w") as file_pointer:
                file_pointer.write(template.substitute(self.config))
