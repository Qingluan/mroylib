import time
from contextlib import contextmanager
from termcolor import cprint

from ._pipe import stdout

_do_some = lambda x: cprint("%s ..." % x, "yellow", end="")
_ok = lambda : cprint("\b\b\b ok", "green", attrs=['bold'])
_err = lambda : cprint("\b\b\b err", "red", attrs=['bold'])


@contextmanager
def just_info(info):
    try:
        _do_some(info)
        with stdout(None):
            yield
    except:
        _err()
    else:
        _ok()
