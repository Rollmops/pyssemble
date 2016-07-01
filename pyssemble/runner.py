import os
from collections import namedtuple

from pyssemble.plugin_loader import PluginLoader
from pyssemble.synchronizer import Synchronizer

Context = namedtuple("Context", ["config"])


class Runner:
    PHASES = ["validate",
              "prepare"
              "precompile",
              "compile",
              "test",
              "package",
              "deploy",
              "install"]

    def __init__(self, config: dict, plugin_loader: PluginLoader):
        self.config = config
        self.plugin_loader = plugin_loader
        self.synchronizer = Synchronizer()

    def init(self, load_base_plugins=True):
        self.plugin_loader.load(self.config)
        if load_base_plugins:
            self.plugin_loader.load_base_plugins()

    def run_phase(self, phase: str):
        context = self._create_context_for_phase(phase)

        for plugin in PluginLoader.PLUGINS:
            if plugin.phase == phase:
                plugin.function(context)

    def _create_context_for_phase(self, phase):
        self.synchronizer.synchronize(os.path.join(self.config["root_path"], "src"), self.config["build_path"])

        context = Context(config=self.config)
        return context
