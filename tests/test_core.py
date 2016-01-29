
from datetime import datetime

import click
import pytest

from click_shell._cmd import ClickCmd
from click_shell.core import Shell, make_click_shell, get_invoke


class TestShell(object):

    def test_create(self):

        shell = Shell()

        assert isinstance(shell, click.MultiCommand)

    def test_invoke_no_args(self):
        shell = Shell()

        ctx = shell.make_context('click-shell-test', args=[])

        with pytest.raises(IOError):
            shell.invoke(ctx)

    def test_invoke_with_args(self):
        shell = Shell()

        # Create a 'foo' command
        @shell.command()
        def foo():
            click.echo('bar')
            return 0

        ctx = shell.make_context('click-shell-test', args=['foo'])

        retcode = shell.invoke(ctx)

        assert retcode == 0


class TestFactory(object):

    def test_fail_on_bad_command(self):
        command = click.Command('test-command')

        ctx = click.Context(command)

        with pytest.raises(AssertionError):
            make_click_shell(ctx)

    def test_with_group(self):
        command = click.Group()

        ctx = click.Context(command)

        shell = make_click_shell(ctx)

        assert isinstance(shell, ClickCmd)

    def test_get_invoke_command(self):
        time_str = str(datetime.now())

        @click.command()
        def test_command():
            click.echo(time_str)
            return time_str

        fun = get_invoke(test_command)

        assert callable(fun)

        ret = fun(None, '')

        # Make sure it returned the correct thing
        assert ret is False

    def test_get_invoke_group(self):
        time_str = str(datetime.now())

        @click.group(invoke_without_command=True)
        def main_level():
            pass

        @main_level.group()
        def test_group():
            pass

        @test_group.command()
        def foo():
            click.echo(time_str)
            return time_str

        @test_group.command()
        def bar():
            click.echo('foo')
            return 'foo'

        fun = get_invoke(test_group)

        assert callable(fun)

        # This should be the help function
        ret = fun(None, '')
        assert ret is False

        # Also help
        ret = fun(None, '--help')
        assert ret is False

        # non-existant
        ret = fun(None, 'foobar')
        assert ret is False

        ret = fun(None, 'foo')
        assert ret is False

        ret = fun(None, 'bar')
        assert ret is False

    def test_get_help(self):
        pass
