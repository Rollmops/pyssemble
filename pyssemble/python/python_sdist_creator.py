import logging
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory

from pyssemble.common.copy_tree import copytree
from pyssemble.python.python_setup_cfg_creator import PythonSetupCfgCreator
from pyssemble.python.python_setup_py_creator import PythonSetupPyCreator
from pyssemble.templater import Templater

LOGGER = logging.getLogger(__name__)


class PythonSDistCreator:
    def __init__(self, config):
        self.config = config

        self.python_setup_py_creator = PythonSetupPyCreator(config)
        self.python_setup_cfg_creator = PythonSetupCfgCreator(config)

    def create(self):
        with TemporaryDirectory() as temp_dir:
            source_lib_path = os.path.join(os.getcwd(), "src", "lib", "python")
            LOGGER.debug("Copying from %s to %s" % (source_lib_path, temp_dir))
            copytree(source_lib_path, temp_dir)

            if os.path.exists("README"):
                shutil.copy("README", temp_dir)

            templater = Templater(temp_dir, self.config)
            templater.substitute()

            self.python_setup_cfg_creator.create(temp_dir)
            self.python_setup_py_creator.create(temp_dir)

            os.chdir(temp_dir)
            subprocess.check_output(["python3", "setup.py", "sdist", "--dist-dir", self.config["project.build_path"]])
