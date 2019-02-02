from click_shell import shell
from click_shell._compat import PY2

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO

## Test shell decorator
def test_shell_decorator(monkeypatch):

    @shell(prompt='app# ')
    def app():
        pass

    stdin = StringIO('exit\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)

    try:
        app()
    except SystemExit:
        pass

    # Verify the context key dictionary 'param' is printed
    assert stdout.getvalue() == 'app# '

## Test with one command
def test_command_decorator(monkeypatch):

    @shell(prompt='app$ ')
    def app_one_command():
        pass

    @app_one_command.command()
    def printer():
        print('printed')

    stdin = StringIO('printer\nquit\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)

    try:
        app_one_command()
    except SystemExit:
        pass

    # Verify the context key dictionary 'param' is printed
    assert stdout.getvalue() == 'app$ printed\napp$ '


## Test with finisher
def test_on_finished(monkeypatch):

    def finisher(ctx):
        print(ctx.obj['param'])

    @shell(prompt='app> ', on_finished=finisher)
    def app_with_finisher():
        pass

    stdin = StringIO('quit\n')
    stdout = StringIO()

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.stdout', stdout)

    try:
        # Declare a dictionary as context.obj
        app_with_finisher(obj = {'param':'value'})
    except SystemExit:
        pass

    # Verify the context key dictionary 'param' is printed
    assert stdout.getvalue() == 'app> value\n'
