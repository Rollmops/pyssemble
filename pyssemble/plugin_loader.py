import importlib
from collections import namedtuple

Plugin = namedtuple("Plugin", ["phase", "name", "function"])


class PluginLoader:
    PLUGINS = []

    BASE_PLUGIN_NAMES = ["config_injector"]

    def load(self, config):
        plugins_to_load = config.get("plugins", [])

        for plugin_name in plugins_to_load:
            self._load_plugin(plugin_name)

    def load_base_plugins(self):
        for plugin_name in PluginLoader.BASE_PLUGIN_NAMES:
            self._load_plugin(plugin_name)

    def _load_plugin(self, plugin_name):
        try:
            self._load_from_global(plugin_name)
        except ImportError:
            try:
                self._load_from_builtin(plugin_name)
            except ImportError:
                raise PluginLoader.PluginNotFoundError("Unable to load plugin '%s'" % plugin_name)

    @staticmethod
    def _load_from_global(plugin_to_load):
        importlib.import_module(plugin_to_load)

    @staticmethod
    def _load_from_builtin(plugin_to_load):
        builtin_plugin_to_load = "pyssemble.plugin." + plugin_to_load
        importlib.import_module(builtin_plugin_to_load)

    class PluginNotFoundError(RuntimeError):
        pass


def register(phase, name):
    def decorator(f):
        plugin = Plugin(phase=phase, name=name, function=f)
        PluginLoader.PLUGINS.append(plugin)
        return f

    return decorator
