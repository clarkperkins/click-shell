
import click
import pytest

from click_shell._cmd import ClickCmd
from click_shell.core import Shell, make_click_shell


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
