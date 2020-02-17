
import os
from cmd import Cmd

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


def test_intro():
    stdin = StringIO('exit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    expected_val = '(Cmd) '

    assert stdout.getvalue() == expected_val

    for test_in in ('foo', 'bar', 'blah\n version 2'):
        stdin = StringIO('exit\n')
        stdout = StringIO()

        cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)
        cmd.cmdloop(test_in)
        expected_val = '{0}\n(Cmd) '.format(test_in)

        assert stdout.getvalue() == expected_val

    os.remove('.history')


def test_prompt():
    stdin = StringIO('exit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.prompt = 'foobar > '

    cmd.cmdloop()

    assert stdout.getvalue() == 'foobar > '

    os.remove('.history')


def test_bad_input():
    stdin = StringIO('foobar\nexit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}{1}\n{0}'.format(ClickCmd.prompt,
                                                     ClickCmd.nocommand % 'foobar')

    os.remove('.history')


def test_empty_input():
    stdin = StringIO('\nexit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}{0}'.format(ClickCmd.prompt)

    os.remove('.history')


def test_quit():
    stdin = StringIO('quit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == ClickCmd.prompt

    os.remove('.history')


def test_exit():
    stdin = StringIO('exit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == ClickCmd.prompt

    os.remove('.history')


def test_on_finished():
    stdin = StringIO('exit\n')
    stdout = StringIO()
    
    def finisher(c):
        stdout.write(c + '#finished\n')

    cmd = ClickCmd(ctx='dummy-ctx', hist_file='.history', on_finished=finisher, stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == ClickCmd.prompt + 'dummy-ctx#finished\n'

    os.remove('.history')


def test_help():
    stdin = StringIO('help\nexit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}\nUndocumented commands:\n' \
                                '======================\n' \
                                'exit  help  quit\n' \
                                '\n{0}'.format(ClickCmd.prompt)

    os.remove('.history')


def test_keyboard_interrupt():
    stdin = BadStringIO('exit\n')
    stdout = StringIO()

    cmd = ClickCmd(hist_file='.history', stdin=stdin, stdout=stdout)

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}\nKeyboardInterrupt\n{0}'.format(ClickCmd.prompt)

    os.remove('.history')
