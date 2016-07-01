import logging

from pyssemble.plugin_loader import register
from pyssemble.runner import Context

LOGGER = logging.getLogger(__name__)


@register(phase="prepare", name="config_injector")
def run(context: Context):
    pass
