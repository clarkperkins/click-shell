"""
click_shell.core

Core functionality for click-shell
"""

import os
import shlex

import click

from ._cmd import ClickCmd


def get_invoke(root_ctx, command):
    """
    Get the Cmd main method from the click command
    :param root_ctx: The root context object
    :param command: The click Command object
    :return: the do_* method for Cmd
    :rtype: function
    """

    assert isinstance(command, click.Command)

    def invoke_(self, arg):  # pylint: disable=unused-argument
        try:
            ret = command.main(args=shlex.split(arg),
                               prog_name=command.name,
                               standalone_mode=False,
                               parent=root_ctx)
            return ret
        except click.ClickException as e:
            # Show the error message
            e.show()
        except click.Abort:
            # We got an EOF or Keyboard interrupt.  Just silence it
            pass
        except SystemExit as e:
            # Catch this an return the code instead. All of click's help commands do a sys.exit(),
            # and that's not ideal when running in a shell.
            return e.code
    return invoke_


def get_help(root_ctx, command):
    """
    Get the Cmd help function from the click command
    :param root_ctx: The root context object
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
        with click.Context(command, info_name=command.name, parent=root_ctx, **extra) as ctx:
            click.echo(ctx.get_help(), color=ctx.color)
    return help_


def get_complete(root_ctx, command):
    """
    Get the Cmd complete function for the click command
    :param root_ctx: The root context object
    :param command: The click Command object
    :return: the complete_* method for Cmd
    :rtype: function
    """

    assert isinstance(command, click.Command)

    if isinstance(command, click.MultiCommand):
        # we have a command with subcommands.  Autocomplete them
        def complete_(self, text, line, begidx, endidx):  # pylint: disable=unused-argument
            return [cmd for cmd in command.list_commands(root_ctx) if cmd.startswith(text)]
    else:
        # No subcommands, so complete with filenames
        def complete_(self, text, line, begidx, endidx):  # pylint: disable=unused-argument
            dir_name, file_name = os.path.split(text)

            final_list = []

            for f in os.listdir(dir_name if dir_name != '' else '.'):
                if f.startswith(file_name):
                    if dir_name != '':
                        f = os.path.join(dir_name, f)

                    final_list.append(f)

            if len(final_list) == 1 and os.path.isdir(final_list[0]):
                final_list[0] = '%s/' % final_list[0]

            return final_list

    return complete_


def make_click_shell(root_ctx, prompt=None, intro=None, hist_file=None):

    # Create our ClickShell class (just a pass for now in case we want to override things later)
    class ClickShell(ClickCmd):
        pass

    if prompt is not None:
        ClickShell.prompt = prompt

    if intro is not None:
        ClickShell.intro = intro

    # set all the click commands
    for name, command in root_ctx.command.commands.items():
        cmd_name = name.replace('-', '_')
        setattr(ClickShell, 'do_%s' % cmd_name, get_invoke(root_ctx, command))
        setattr(ClickShell, 'help_%s' % cmd_name, get_help(root_ctx, command))
        setattr(ClickShell, 'complete_%s' % cmd_name, get_complete(root_ctx, command))

    return ClickShell(hist_file=hist_file)


class Shell(click.Group):

    def __init__(self, prompt=None, intro=None, hist_file=None, **attrs):
        self.prompt = prompt
        self.intro = intro
        self.hist_file = hist_file
        attrs['invoke_without_command'] = True
        super(Shell, self).__init__(**attrs)

    def invoke(self, ctx):
        # Grab the parent function first.  If there was no command passed, this
        # shouldn't do anything bad, we just want to capture the retcode
        ret = super(Shell, self).invoke(ctx)

        if not ctx.protected_args and not ctx.invoked_subcommand:
            # Start up the shell
            shell = make_click_shell(ctx, self.prompt, self.intro, self.hist_file)
            shell.cmdloop()

        return ret
