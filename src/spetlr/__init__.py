"""
A common set of python libraries for spark etl.
See https://github.com/spetlr/spetlr for details
"""

from spetlr import etl, functions, spark, sql  # noqa: F401
from spetlr.configurator.configurator import Configurator  # noqa: F401

from .version import __version__  # noqa: F401

DEBUG = False


def dbg(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
