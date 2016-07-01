import collections


def flatten(dictionary, parent_key="", sep="."):
    items = []
    for k, v in dictionary.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class NoBuildConfigFileError(RuntimeError):
    pass


class NoConfigReaderStrategyError(RuntimeError):
    pass


class MultipleBuildConfigFilesError(RuntimeError):
    pass
