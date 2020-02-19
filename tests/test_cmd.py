import os
import sys
from cmd import Cmd

import click

from click_shell._cmd import ClickCmd
from click_shell._compat import PY2

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO


class BadStringIO(StringIO, object):
    def __init__(self, *args, **kwargs):
        super(BadStringIO, self).__init__(*args, **kwargs)
        self.first = True

    def read(self, *args, **kwargs):
        if self.first:
            self.first = False
            raise KeyboardInterrupt()
        return super(BadStringIO, self).read(*args, **kwargs)

    def readline(self, *args, **kwargs):
        if self.first:
            self.first = False
            raise KeyboardInterrupt()
        return super(BadStringIO, self).readline(*args, **kwargs)


def test_create():
    cmd = ClickCmd()

    # Make sure it's a Cmd
    assert isinstance(cmd, Cmd)

    # Make sure it's a new-style class
    assert isinstance(cmd, object)

    # Make sure we have our exit functions
    assert hasattr(cmd, 'do_quit')
    assert hasattr(cmd, 'do_exit')


def test_intro_default(cli_runner):
    with cli_runner.isolation() as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == '(Cmd) \n'
    os.remove('.history')


def test_intro_custom(cli_runner):
    for test_in in ('foo', 'bar', 'blah\n version 2'):
        with cli_runner.isolation() as outstreams:
            cmd = ClickCmd(hist_file='.history')
            cmd.cmdloop(test_in)

            output = outstreams[0].getvalue() \
                .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

        assert output == '{0}\n(Cmd) \n'.format(test_in)

    os.remove('.history')


def test_prompt(cli_runner):
    with cli_runner.isolation() as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.prompt = 'foobar > '

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == 'foobar > \n'

    os.remove('.history')


def test_bad_input(cli_runner):
    with cli_runner.isolation(input='foobar\n') as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == '{0}{1}\n{0}\n'.format(ClickCmd.prompt,
                                            ClickCmd.nocommand % 'foobar')

    os.remove('.history')


def test_empty_input(cli_runner):
    with cli_runner.isolation(input='\n') as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == '{0}{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')


def test_quit(cli_runner):
    with cli_runner.isolation(input='quit\n') as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == ClickCmd.prompt

    os.remove('.history')


def test_exit(cli_runner):
    with cli_runner.isolation(input='exit\n') as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == ClickCmd.prompt

    os.remove('.history')


def test_on_finished(cli_runner):
    with cli_runner.isolation() as outstreams:
        def finisher(c):
            click.echo(c + '#finished')

        cmd = ClickCmd(ctx='dummy-ctx', hist_file='.history', on_finished=finisher)

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == ClickCmd.prompt + '\ndummy-ctx#finished\n'

    os.remove('.history')


def test_help(cli_runner):
    with cli_runner.isolation(input='help\n') as outstreams:
        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == '{0}\n' \
                     'Undocumented commands:\n' \
                     '======================\n' \
                     'exit  help  quit\n' \
                     '\n' \
                     '{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')


def test_keyboard_interrupt():
    stdin = BadStringIO()
    stdout = StringIO()

    old_in = sys.stdin
    old_out = sys.stdout
    try:
        sys.stdin = stdin
        sys.stdout = stdout

        cmd = ClickCmd(hist_file='.history')

        cmd.cmdloop()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out

    assert stdout.getvalue() == '{0}\nKeyboardInterrupt\n{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')


def test_changable_prompt(cli_runner):
    with cli_runner.isolation(input='\n\n\n') as outstreams:

        cmd = ClickCmd(hist_file='.history')

        class Prompt(object):

            def __init__(self):
                self.num = 0

            def __call__(self):
                self.num += 1
                return "prompt #{} > ".format(self.num)

        cmd.prompt = Prompt()

        cmd.cmdloop()

        output = outstreams[0].getvalue() \
            .decode(cli_runner.charset, 'replace').replace('\r\n', '\n')

    assert output == 'prompt #1 > prompt #2 > prompt #3 > prompt #4 > \n'

    os.remove('.history')
