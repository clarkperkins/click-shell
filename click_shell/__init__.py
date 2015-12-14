"""
click-shell

An extension to click that easily turns your click app into a shell utility
"""

from click_shell.core import make_click_shell
from click_shell.decorators import shell


__version__ = '0.1.0'

__all__ = [
    'make_click_shell',
    'shell',
]
