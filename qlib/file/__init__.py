from .__file import to_save, call_vim, file_search

__all__ = [
    'to_save',
    'call_vim',
    'file_search',
    'j',
]


def j(*paths):
    import os
    from functools import reduce
    return reduce(os.path.join, paths)