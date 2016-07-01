import logging
from tempfile import TemporaryDirectory

from pyssemble.plugin_loader import register

LOGGER = logging.getLogger(__name__)


@register(phase="distribute", name="python_sdist_plugin")
def sdist(context):
    with TemporaryDirectory() as temp_dir:
        pass
