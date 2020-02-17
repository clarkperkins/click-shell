"""
click_shell.core

Core functionality for click-shell
"""

import logging
import shlex
import traceback
from functools import update_wrapper
from logging import NullHandler

import click

from ._cmd import ClickCmd
from ._compat import get_method_type, get_choices

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def get_invoke(command):
    """
    Get the Cmd main method from the click command
    :param command: The click Command object
    :return: the do_* method for Cmd
    :rtype: function
    """

    assert isinstance(command, click.Command)

    def invoke_(self, arg):  # pylint: disable=unused-argument
        try:
            command.main(args=shlex.split(arg),
                         prog_name=command.name,
                         standalone_mode=False,
                         parent=self.ctx)
        except click.ClickException as e:
            # Show the error message
            e.show()
        except click.Abort:
            # We got an EOF or Keyboard interrupt.  Just silence it
            pass
        except SystemExit:
            # Catch this an return the code instead. All of click's help commands do a sys.exit(),
            # and that's not ideal when running in a shell.
            pass
        except Exception as e:
            traceback.print_exception(type(e), e, None)
            logger.warning(traceback.format_exc())

        # Always return False so the shell doesn't exit
        return False

    invoke_ = update_wrapper(invoke_, command.callback)
    invoke_.__name__ = 'do_%s' % command.name
    return invoke_


def get_help(command):
    """
    Get the Cmd help function from the click command
    :param command: The click Command object
    :return: the help_* method for Cmd
    :rtype: function
    """
    assert isinstance(command, click.Command)

    def help_(self):  # pylint: disable=unused-argument
        extra = {}
        for key, value in command.context_settings.items():
            if key not in extra:
                extra[key] = value

        # Print click's help message
        with click.Context(command, info_name=command.name, parent=self.ctx, **extra) as ctx:
            click.echo(ctx.get_help(), color=ctx.color)

    help_.__name__ = 'help_%s' % command.name
    return help_


def get_complete(command):
    """
    Get the Cmd complete function for the click command
    :param command: The click Command object
    :return: the complete_* method for Cmd
    :rtype: function
    """

    assert isinstance(command, click.Command)

    def complete_(self, text, line, begidx, endidx):  # pylint: disable=unused-argument
        # Parse the args
        args = shlex.split(line[:begidx])
        # Strip of the first item which is the name of the command
        args = args[1:]

        # Then pass them on to the get_choices method that click uses for completion
        return [choice[0] if isinstance(choice, tuple) else choice
                for choice in get_choices(command, command.name, args, text)]

    complete_.__name__ = 'complete_%s' % command.name
    return complete_


class ClickShell(ClickCmd):

    def add_command(self, cmd, name):
        # Use the MethodType to add these as bound methods to our current instance
        setattr(self, 'do_%s' % name, get_method_type(get_invoke(cmd), self))
        setattr(self, 'help_%s' % name, get_method_type(get_help(cmd), self))
        setattr(self, 'complete_%s' % name, get_method_type(get_complete(cmd), self))


def make_click_shell(ctx, prompt=None, intro=None, hist_file=None):
    assert isinstance(ctx, click.Context)
    assert isinstance(ctx.command, click.MultiCommand)

    # Set this to None so that it doesn't get printed out in usage messages
    ctx.info_name = None

    # Create our shell object
    shell = ClickShell(ctx=ctx, hist_file=hist_file)

    if prompt is not None:
        shell.prompt = prompt

    if intro is not None:
        shell.intro = intro

    # Add all the commands
    for name in ctx.command.list_commands(ctx):
        command = ctx.command.get_command(ctx, name)
        shell.add_command(command, name)

    return shell


class Shell(click.Group):

    def __init__(self, prompt=None, intro=None, hist_file=None, on_finished=None, **attrs):
        attrs['invoke_without_command'] = True
        super(Shell, self).__init__(**attrs)

        # Make our shell
        self.shell = ClickShell(hist_file=hist_file, on_finished=on_finished)
        if prompt:
            self.shell.prompt = prompt
        self.shell.intro = intro

    def add_command(self, cmd, name=None):
        super(Shell, self).add_command(cmd, name)

        # Grab the proper name
        name = name or cmd.name

        # Add the command to the shell
        self.shell.add_command(cmd, name)

    def invoke(self, ctx):
        # Call super() first.  This ensures that we call the method body of our instance first,
        # in case it's something other than `pass`
        ret = super(Shell, self).invoke(ctx)

        if not ctx.protected_args and not ctx.invoked_subcommand:
            # Set this to None so that it doesn't get printed out in usage messages
            ctx.info_name = None

            # Set the context on the shell
            self.shell.ctx = ctx

            # Start up the shell
            return self.shell.cmdloop()

        return ret
