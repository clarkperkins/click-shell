
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


def test_intro(monkeypatch):
    stdin = StringIO()
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    expected_val = '(Cmd) \n'

    assert stdout.getvalue() == expected_val

    for test_intro in ('foo', 'bar', 'blah\n version 2'):
        cmd.cmdloop(test_intro)
        expected_val += '{0}\n(Cmd) \n'.format(test_intro)

        assert stdout.getvalue() == expected_val

    os.remove('.history')


def test_prompt(monkeypatch):
    stdin = StringIO()
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.prompt = 'foobar > '

    cmd.cmdloop()

    assert stdout.getvalue() == 'foobar > \n'

    os.remove('.history')


def test_bad_input(monkeypatch):
    stdin = StringIO('foobar\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}{1}\n{0}\n'.format(ClickCmd.prompt,
                                                       ClickCmd.nocommand % 'foobar')

    os.remove('.history')


def test_empty_input(monkeypatch):
    stdin = StringIO('\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')


def test_quit(monkeypatch):
    stdin = StringIO('quit\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == ClickCmd.prompt

    os.remove('.history')


def test_exit(monkeypatch):
    stdin = StringIO('exit\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == ClickCmd.prompt

    os.remove('.history')


def test_help(monkeypatch):
    stdin = StringIO('help\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}\nUndocumented commands:\n' \
                                '======================\n' \
                                'exit  help  quit\n' \
                                '\n{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')


def test_keyboard_interrupt(monkeypatch):
    stdin = BadStringIO()
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)
    cmd = ClickCmd(hist_file='.history')

    cmd.cmdloop()

    assert stdout.getvalue() == '{0}\nKeyboardInterrupt\n{0}\n'.format(ClickCmd.prompt)

    os.remove('.history')
