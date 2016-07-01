import os

from pyssemble.dotted_template import DottedTemplate

SETUP_PY_TEMPLATE = '''
from setuptools import setup, find_packages

setup(
name="${project.name}",
version="${project.version}",
author="${project.author}",
author_email="${project.author_email}",
url="${project.url}",
packages=find_packages(),
{additional_options}
)
'''


class PythonSetupPyCreator:
    FILE_NAME = "setup.py"

    def __init__(self, config):
        self.config = config

    def create(self, directory):
        setup_py_template = DottedTemplate(SETUP_PY_TEMPLATE)
        setup_py = setup_py_template.substitute(self.config)

        additional_options = self._get_additional_options()
        setup_py = setup_py.format(additional_options=additional_options)

        with open(os.path.join(directory, PythonSetupPyCreator.FILE_NAME), "w") as setup_py_pointer:
            setup_py_pointer.write(setup_py)

    def _get_additional_options(self):
        additional_options = ""
        if "python.namespace_packages" in self.config:
            additional_options = "namespace_packages=%s" % self.config["python.namespace_packages"]

        return additional_options
