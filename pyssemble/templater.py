import fnmatch
import logging
import os

from pyssemble.dotted_template import DottedTemplate

LOGGER = logging.getLogger(__name__)


class Templater:
    def __init__(self, path, config):
        self.path = path
        self.config = config

    def substitute(self):
        for file in Templater.recursive_iterate(self.path):
            with open(file) as file_pointer:
                content = file_pointer.read()
            template = DottedTemplate(content)
            with open(file, "w") as file_pointer:
                file_pointer.write(template.substitute(self.config))

    @staticmethod
    def recursive_iterate(path, pattern="*"):
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, pattern):
                yield os.path.join(root, filename)
