import os

from pyssemble.dotted_template import DottedTemplate

SETUP_CFG_TEMPLATE = """
[install]
prefix = ${project.prefix}
"""


class PythonSetupCfgCreator:
    def __init__(self, config):
        self.config = config

    def create(self, directory):
        setup_cfg_template = DottedTemplate(SETUP_CFG_TEMPLATE)

        with open(os.path.join(directory, "setup.cfg"), "w") as setup_cfg_pointer:
            setup_cfg_pointer.write(setup_cfg_template.substitute(self.config))
