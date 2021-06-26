"""
click-shell

An extension to click that easily turns your click app into a shell utility
"""

from .core import make_click_shell, Shell
from .decorators import shell

__all__ = [
    'make_click_shell',
    'shell',
    'Shell',
    '__version__',
]

__version__ = "2.1"
