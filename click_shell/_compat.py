"""
click_shell._compat

Compatibility things for python 2.6
"""

# pylint: disable=unused-import, wrong-import-position

import sys
import types

PY2 = sys.version_info[0] == 2

try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        readline = None


def get_method_type(func, obj):
    if PY2:
        return types.MethodType(func, obj, type(obj))
    else:
        return types.MethodType(func, obj)


try:
    from click._bashcomplete import get_choices

except ImportError:

    import click
    from click._bashcomplete import resolve_ctx

    def get_choices(cli, prog_name, args, incomplete):
        """
        This is identical to click._bashcomplete:get_choices in click 6.4+
        """
        ctx = resolve_ctx(cli, prog_name, args)

        if ctx is None:
            return

        choices = []
        if incomplete and not incomplete[:1].isalnum():
            for param in ctx.command.params:
                if not isinstance(param, click.Option):
                    continue
                choices.extend(param.opts)
                choices.extend(param.secondary_opts)
        elif isinstance(ctx.command, click.MultiCommand):
            choices.extend(ctx.command.list_commands(ctx))

        for item in choices:
            if item.startswith(incomplete):
                yield item
