import logging
import os
import shutil

from pyssemble.common.recursive_path_iterate import recursive_path_iterate

LOGGER = logging.getLogger(__name__)


class Synchronizer:
    @staticmethod
    def synchronize(source, dest, pattern="*"):
        LOGGER.debug("synchronizing '%s' to '%s'" % (source, dest))
        for abs_source_path in recursive_path_iterate(source, pattern):
            rel_path_to_sync = os.path.relpath(abs_source_path, source)

            abs_dest_path = os.path.join(dest, rel_path_to_sync)

            if Synchronizer._is_sync_needed(abs_source_path, abs_dest_path):
                os.makedirs(os.path.dirname(abs_dest_path), exist_ok=True)
                shutil.copy(abs_source_path, abs_dest_path)

    @staticmethod
    def _is_sync_needed(abs_source_path, abs_dest_path):

        if not os.path.exists(abs_dest_path):
            return True

        modification_time_source = os.stat(abs_source_path).st_mtime
        modification_time_dest = os.stat(abs_dest_path).st_mtime

        if modification_time_source > modification_time_dest:
            return True
