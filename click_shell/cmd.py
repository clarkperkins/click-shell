"""
click_shell._cmd

This module overrides the builtin python cmd module
"""

import inspect
import os
from cmd import Cmd
from typing import Any, Callable, List, Optional, Union

import click

from ._compat import readline


class CommandChainException(Exception):
    pass


class Command:
    INITIAL = 'INITIAL'
    AND = 'AND'
    OR = 'OR'

    def __init__(self, command: str, cmd_type: Union[AND, OR, INITIAL]):
        self.text = command
        self.cmd_type = cmd_type


class CommandQueue(List):
    """
    ClickCmd expects a List, so we implement our own with parsing
    """

    def __init__(self):
        super().__init__()
        self.queue = list()

    def parse_line(self, *, line: str):
        initial_command = True
        for command in line.split("&&"):
            command = command.strip()
            if initial_command:
                self.queue.append(Command(command=command, cmd_type=Command.INITIAL))
                initial_command = False
                continue
            if '||' not in command:
                self.queue.append(Command(command=command, cmd_type=Command.AND))
            else:
                first = True
                for _command in command.split("||"):
                    _command = _command.strip()
                    if first:
                        self.queue.append(Command(command=_command, cmd_type=Command.AND))
                        first = False
                        continue
                    self.queue.append(Command(command=_command, cmd_type=Command.OR))

    def pop(self, __index: int = ...):
        return self.queue.pop(__index)

    def flush(self) -> None:
        """
        Flushes out the queue by setting the property to an empty list
        :return:
        """
        self.queue = list()

    def __len__(self) -> int:
        """
        :return: int length of self.queue
        """
        return len(self.queue)


class ClickCmd(Cmd):
    """
    A simple wrapper around the builtin python cmd module that:
    1) makes completion work on OSX
    2) uses a history file
    3) uses click.echo instead of std*.write()
    """

    # Allow dashes
    identchars = Cmd.identchars + '-'

    nohelp = "No help on %s"
    nocommand = "Command not found: %s"

    prompt: Optional[Union[str, Callable[..., str]]] = Cmd.prompt  # type: ignore

    def __init__(
            self,
            ctx: Optional[click.Context] = None,
            hist_file: Optional[str] = None,
            *args,
            **kwargs,
    ):
        # Never allow super() to default to sys.stdout for stdout.
        # Instead pass along a wrapper that delegates to click.echo().
        self._stdout = kwargs.get('stdout')

        super().__init__(*args, **kwargs)

        self.old_completer: Optional[Callable] = None
        self.old_delims: Optional[str] = None

        # We need to save the context!!
        self.ctx: Optional[click.Context] = ctx

        # Set the history file
        hist_file = hist_file or os.path.join(os.path.expanduser('~'), '.click-history')
        self.hist_file: str = os.path.abspath(hist_file)

        # Make the parent directory
        if not os.path.isdir(os.path.dirname(self.hist_file)):
            os.makedirs(os.path.dirname(self.hist_file))

        self.cmdqueue = CommandQueue()

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

    # We need to override this to fix readline
    def cmdloop(self, intro: str = None):  # pylint: disable=too-many-branches
        self.preloop()
        if self.completekey and readline:
            self.old_completer = readline.get_completer()
            self.old_delims = readline.get_completer_delims()
            readline.set_completer(self.complete)  # type: ignore
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
                click.echo(self.intro, file=self._stdout)
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    try:
                        line = input(self.get_prompt())
                    except EOFError:
                        # We just want to quit here instead of changing the arg to EOF
                        click.echo(file=self._stdout)
                        break
                    except KeyboardInterrupt:
                        # We don't want to exit the shell on a keyboard interrupt
                        click.echo(file=self._stdout)
                        click.echo('KeyboardInterrupt', file=self._stdout)
                        continue
                try:
                    line = self.precmd(line)
                    stop = self.onecmd(line)
                    stop = self.postcmd(stop, line)
                except CommandChainException:
                    self.cmdqueue.flush()

        finally:
            self.postloop()
            if self.completekey and readline:
                if self.old_completer:
                    readline.set_completer(self.old_completer)
                if self.old_delims:
                    readline.set_completer_delims(self.old_delims)

    def precmd(self, line: Union[str, Command]) -> str:
        if isinstance(line, str):
            if any([chain in line for chain in ["&&", "||"]]):
                self.cmdqueue.parse_line(line=line)
                line = self.cmdqueue.pop(0).text
        if isinstance(line, Command):
            # a non-zero return code followed by and AND-ed command
            if self.ctx.return_code and line.cmd_type == Command.AND:  # noqa: return_code set in initial context
                raise CommandChainException
            # a zero return code followed by an OR-ed command
            elif not self.ctx.return_code and line.cmd_type == Command.OR:  # noqa: return_code set in initial context
                raise CommandChainException
            else:
                line = line.text

        return line

    def get_prompt(self) -> Optional[str]:
        if callable(self.prompt):
            kwargs = {}
            if hasattr(inspect, 'signature'):
                sig = inspect.signature(self.prompt)
                if 'ctx' in sig.parameters:
                    kwargs['ctx'] = self.ctx
            return self.prompt(**kwargs)
        else:
            return self.prompt

    def emptyline(self) -> bool:
        # we don't want to repeat the last command if nothing was typed
        return False

    def default(self, line: str):
        click.echo(self.nocommand % line, file=self._stdout)

    def get_names(self) -> List[str]:
        # Do dir(self) instead of dir(self.__class__)
        return dir(self)

    def do_help(self, arg: str):
        if not arg:
            super().do_help(arg)
            return

        # Override to give better error message
        try:
            func = getattr(self, 'help_' + arg)
        except AttributeError:
            try:
                do_fun = getattr(self, 'do_' + arg, None)

                if do_fun is None:
                    click.echo(self.nocommand % arg, file=self._stdout)
                    return

                doc = do_fun.__doc__
                if doc:
                    click.echo(doc, file=self._stdout)
                    return
            except AttributeError:
                pass
            click.echo(self.nohelp % arg, file=self._stdout)
            return
        func()

    def do_quit(self, arg) -> bool:  # pylint: disable=unused-argument,no-self-use
        return True

    def do_exit(self, arg) -> bool:  # pylint: disable=unused-argument,no-self-use
        return True

    def print_topics(self, header: Any, cmds: Optional[List[str]], cmdlen: int, maxcol: int):
        if cmds:
            click.echo(header, file=self._stdout)
            if self.ruler:
                click.echo(str(self.ruler * len(header)), file=self._stdout)
            self.columnize(cmds, maxcol - 1)
            click.echo(file=self._stdout)
