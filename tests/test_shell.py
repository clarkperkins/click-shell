
import click

import click_shell
from click_shell._compat import PY2

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO


# Test shell decorator
def test_shell_decorator(cli_runner):

    @click_shell.shell(prompt='app# ')
    def app():
        pass

    result = cli_runner.invoke(app, input='exit\n')

    # Verify the context key dictionary 'param' is printed
    assert result.output == 'app# '


# Test with one command
def test_command_decorator(cli_runner):

    @click_shell.shell(prompt='app$ ')
    def app_one_command():
        pass

    @app_one_command.command()
    def printer():
        click.echo('printed')

    result = cli_runner.invoke(app_one_command, input='printer\nexit\n')

    # Verify the context key dictionary 'param' is printed
    assert result.output == 'app$ printed\napp$ '


# Test with finisher
def test_on_finished(cli_runner):

    def finisher(ctx):
        click.echo(ctx.obj['param'])

    @click_shell.shell(prompt='app> ', on_finished=finisher)
    def app_with_finisher():
        pass

    result = cli_runner.invoke(app_with_finisher, input='exit\n', obj={'param': 'value'})

    # Verify the context key dictionary 'param' is printed
    assert result.output == 'app> value\n'
