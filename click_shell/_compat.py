"""
click_shell._compat

Compatibility things for readline + various versions of click
"""

# pylint: disable=unused-import, wrong-import-position

from typing import List

import click

try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        readline = None

try:
    # Click 8
    from click.shell_completion import ShellComplete


    # Wrapper around the new completion system in click 8
    def get_choices(
            cli: click.BaseCommand,
            prog_name: str,
            args: List[str],
            incomplete: str
    ) -> List[str]:
        comp = ShellComplete(cli, {}, prog_name, "")
        return [c.value for c in comp.get_completions(args, incomplete)]

except ImportError:
    # Click 7
    from click._bashcomplete import get_choices
