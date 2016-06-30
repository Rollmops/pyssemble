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
namespace_packages=["pcs"],
packages=find_packages())
'''


class PythonSetupPyCreator:
    def __init__(self, config):
        self.config = config

    def create(self, directory):
        setup_py_template = DottedTemplate(SETUP_PY_TEMPLATE)

        with open(os.path.join(directory, "setup.py"), "w") as setup_py_pointer:
            setup_py_pointer.write(setup_py_template.substitute(self.config))
