"""
click_shell.decorators

Decorators to make using click_shell simpler and more similar to click.
"""

from typing import Any, Callable, Optional, TypeVar, cast

import click

from .core import Shell

F = TypeVar("F", bound=Callable[..., Any])


def shell(name: Optional[str] = None, **attrs: Any) -> Callable[[F], Shell]:
    """Creates a new :class:`Shell` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Shell`.
    """
    attrs.setdefault('cls', Shell)
    return cast(Shell, click.command(name, **attrs))
