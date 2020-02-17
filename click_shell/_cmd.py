"""
click_shell._cmd

This module overrides the builtin python cmd module
"""

import inspect
import os
import sys
from cmd import Cmd

import click
from click._compat import _default_text_stdin, _default_text_stdout

from click_shell._compat import readline


def get_input(prompt, stdin, stdout):
    sys.stderr.flush()
    if prompt:
        _stdout = stdout
        if not _stdout:
            _stdout = _default_text_stdout()

        _stdout.write(prompt)
        _stdout.flush()

    _stdin = stdin
    if not _stdin:
        _stdin = _default_text_stdin()

    ret = _stdin.readline().rstrip('\r\n')
    return ret


class ClickCmd(Cmd, object):
    """
    A simple wrapper around the builtin python cmd module that:
    1) makes completion work on OSX
    2) uses a history file
    3) uses click.echo instead of std*.write()
    4) turns Cmd into a new-style python object :)
    """

    # Allow dashes
    identchars = Cmd.identchars + '-'

    nohelp = "No help on %s"
    nocommand = "Command not found: %s"

    def __init__(self, ctx=None, on_finished=None, hist_file=None,
                 stdin=None, stdout=None, *args, **kwargs):
        super(ClickCmd, self).__init__(*args, **kwargs)

        # yes, this does overwrite the stdin/stdout that get set by super().
        # But we want these to default to None, so that the get_input() method
        # above will handle things correctly.
        self.stdin = stdin
        self.stdout = stdout

        self.old_completer = None
        self.old_delims = None

        # We need to save the context!!
        self.ctx = ctx
        self.on_finished = on_finished

        # Set the history file
        hist_file = hist_file or os.path.join(os.path.expanduser('~'), '.click-history')
        self.hist_file = os.path.abspath(hist_file)

        # Make the parent directory
        if not os.path.isdir(os.path.dirname(self.hist_file)):
            os.makedirs(os.path.dirname(self.hist_file))

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
            readline.set_history_length(1000)
            try:
                readline.write_history_file(self.hist_file)
            except IOError:
                pass

        # Finisher callback on the context
        if self.on_finished:
            self.on_finished(self.ctx)

    # We need to override this to fix readline
    def cmdloop(self, intro=None):  # pylint: disable=too-many-branches
        self.preloop()
        if self.completekey and readline:
            self.old_completer = readline.get_completer()
            self.old_delims = readline.get_completer_delims()
            readline.set_completer(self.complete)
            readline.set_completer_delims(' \n\t')
            to_parse = self.completekey + ': complete'
            if readline.__doc__ and 'libedit' in readline.__doc__:
                # Special case for mac OSX
                to_parse = 'bind ^I rl_complete'
            readline.parse_and_bind(to_parse)
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                click.echo(self.intro, file=self.stdout)
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    try:
                        line = get_input(self.get_prompt(), self.stdin, self.stdout)
                    except EOFError:
                        # We just want to quit here instead of changing the arg to EOF
                        click.echo(file=self.stdout)
                        break
                    except KeyboardInterrupt:
                        # We don't want to exit the shell on a keyboard interrupt
                        click.echo(file=self.stdout)
                        click.echo('KeyboardInterrupt', file=self.stdout)
                        continue
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)

        finally:
            self.postloop()
            if self.completekey and readline:
                readline.set_completer(self.old_completer)
                readline.set_completer_delims(self.old_delims)

    def get_prompt(self):
        if callable(self.prompt):
            sig = inspect.signature(self.prompt)
            kwargs = {}
            if 'ctx' in sig.parameters:
                kwargs['ctx'] = self.ctx
            return self.prompt(**kwargs)
        else:
            return self.prompt

    def emptyline(self):
        # we don't want to repeat the last command if nothing was typed
        return False

    def default(self, line):
        click.echo(self.nocommand % line, file=self.stdout)

    def get_names(self):
        # Do dir(self) instead of dir(self.__class__)
        return dir(self)

    def do_help(self, arg):
        if not arg:
            super(ClickCmd, self).do_help(arg)

        # Override to give better error message
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

    def do_quit(self, arg):  # pylint: disable=unused-argument,no-self-use
        return True

    def do_exit(self, arg):  # pylint: disable=unused-argument,no-self-use
        return True

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            click.echo(header, file=self.stdout)
            if self.ruler:
                click.echo(str(self.ruler * len(header)), file=self.stdout)
            self.columnize(cmds, maxcol - 1)
            click.echo(file=self.stdout)
