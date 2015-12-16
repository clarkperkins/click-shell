
from cmd import Cmd

from click_shell._cmd import ClickCmd


def test_create():
    cmd = ClickCmd()

    # Make sure it's a Cmd
    assert isinstance(cmd, Cmd)

    # Make sure it's a new-style class
    assert isinstance(cmd, object)

    # Make sure we have our exit functions
    assert hasattr(cmd, 'do_quit')
    assert hasattr(cmd, 'do_exit')


def test_loop():
    pass
