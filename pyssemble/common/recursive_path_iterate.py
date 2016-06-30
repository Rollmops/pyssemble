import fnmatch
import os


def recursive_path_iterate(path, pattern):
    for root, dir_names, file_names in os.walk(path):
        for filename in fnmatch.filter(file_names, pattern):
            yield os.path.join(root, filename)
