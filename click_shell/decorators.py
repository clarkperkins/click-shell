"""
click_shell.decorators

Decorators to make using click_shell simpler and more similar to click.
"""

import click

from .core import make_click_shell


def shell(prompt=None, intro=None, hist_file=None, **attrs):
    def wrapper(func):

        # We're going to drop this in to the group as it's callback
        def new_func(*args, **kwargs):

            # Grab the current context (this is what @click.pass_context does)
            ctx = click.get_current_context()

            if ctx.invoked_subcommand is None:
                # If there's no command, launch a shell
                shell_obj = make_click_shell(
                    ctx,
                    prompt=prompt,
                    intro=intro,
                    hist_file=hist_file,
                )
                shell_obj.cmdloop()

            # Be sure to call the original func
            func(*args, **kwargs)

        # Override this param
        attrs.setdefault('invoke_without_command', True)

        return click.group(**attrs)(new_func)
    return wrapper
