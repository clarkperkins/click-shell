"""
click_shell._cmd

This module overrides the builtin python cmd module
"""

import os
import sys
from cmd import Cmd

try:
    import readline
except ImportError:
    readline = None

import click

PY3 = sys.version_info[0] == 3

# python 3 compatibility
if PY3:
    raw_input = input  # pylint: disable=invalid-name,redefined-builtin


class ClickCmd(Cmd, object):
    """
    A simple wrapper around the builtin python cmd module that:
    1) makes completion work on OSX
    2) uses a history file
    3) uses click.echo instead of std*.write()
    4) turns Cmd into a new-style python object :)
    """

    nohelp = "No help on %s"
    nocommand = "Command not found: %s"

    def __init__(self, hist_file=None, *args, **kwargs):
        super(ClickCmd, self).__init__(*args, **kwargs)
        self.old_completer = None

        if hist_file is None:
            hist_file = os.path.join(os.path.expanduser('~'), '.click-history')

        self.hist_file = hist_file

    def preloop(self):
        # read our history
        if readline:
            try:
                readline.read_history_file(self.hist_file)
            except IOError:
                pass

    def postloop(self):
        # Write our history
        if readline:
            readline.write_history_file(self.hist_file)

    # We need to override this to fix readline
    def cmdloop(self, intro=None):  # pylint: disable=too-many-branches
        self.preloop()
        if self.use_rawinput and self.completekey and readline:
            self.old_completer = readline.get_completer()
            readline.set_completer(self.complete)
            if 'libedit' in readline.__doc__:
                # For mac OSX
                readline.parse_and_bind('bind ^I rl_complete')
            else:
                # for other platforms
                readline.parse_and_bind(self.completekey + ': complete')
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                click.echo(self.intro, file=self.stdout)
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                elif self.use_rawinput:
                    try:
                        line = raw_input(self.prompt)
                    except EOFError:
                        # We just want to quit here instead of changing the arg to
                        click.echo(file=self.stdout)
                        break
                    except KeyboardInterrupt:
                        # We don't want to exit the shell on a keyboard interrupt
                        click.echo(file=self.stdout)
                        click.echo('KeyboardInterrupt', file=self.stdout)
                        continue
                else:
                    click.echo(self.prompt, file=self.stdout)
                    line = self.stdin.readline()
                    if not len(line):
                        line = 'EOF'
                    else:
                        line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)

        finally:
            self.postloop()
            if self.use_rawinput and self.completekey and readline:
                readline.set_completer(self.old_completer)

    def emptyline(self):
        # we don't want to repeat the last command if nothing was typed
        return False

    def default(self, line):
        click.echo(self.nocommand % line, file=self.stdout)

    def do_help(self, arg):
        # Override to give better error message
        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    do_fun = getattr(self, 'do_' + arg, None)

                    if do_fun is None:
                        click.echo(self.nocommand % arg, file=self.stdout)
                        return

                    doc = do_fun.__doc__
                    if doc:
                        click.echo(doc, file=self.stdout)
                        return
                except AttributeError:
                    pass
                click.echo(self.nohelp % arg, file=self.stdout)
                return
            func()
        else:
            return super(ClickCmd, self).do_help(arg)

    def do_quit(self, arg):  # pylint: disable=unused-argument,no-self-use
        return True

    def do_exit(self, arg):  # pylint: disable=unused-argument,no-self-use
        return True
