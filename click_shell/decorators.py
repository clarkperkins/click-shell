"""
click_shell.decorators

Decorators to make using click_shell simpler and more similar to click.
"""

import click

from .core import Shell


def shell(name=None, **attrs):
    """Creates a new :class:`Shell` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Shell`.
    """
    attrs.setdefault('cls', Shell)
    return click.command(name, **attrs)
