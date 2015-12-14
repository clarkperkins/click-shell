"""
click_shell.decorators

Decorators to make using click_shell simpler and more similar to click.
"""


import click

from .core import make_click_shell


def shell(prompt=None, intro=None, hist_file=None):
    def wrapper(func):
        def inner_func(ctx, *args, **kwargs):
            assert isinstance(ctx, click.Context), (
                'Make sure your root level group is decorated with '
                '`@click.pass_context` and has `ctx` as the first argument'
            )

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
            func(ctx, *args, **kwargs)

        return inner_func
    return wrapper
