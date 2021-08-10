"""
click-shell

An extension to click that easily turns your click app into a shell utility
"""

from .core import make_click_shell, Shell, ClickShell
from .decorators import shell

__all__ = [
    'make_click_shell',
    'shell',
    'Shell',
    'ClickShell',
    '__version__',
]

__version__ = "3.0.dev1"
