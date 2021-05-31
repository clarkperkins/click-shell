
import pytest
import click

from click_shell.exceptions import ClickShellUncleanExit, ClickShellCleanExit
from click_shell.core import Shell,  get_invoke


try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock


@pytest.fixture
def mock_cli_command():
    shell = Shell()

    @shell.command()
    def mock_command():
        pass

    return mock_command


@patch('click.Command.main')
def test_unclean_exit_default_code(m_main, mock_cli_command):

    expected_error_code = ClickShellUncleanExit.default_error_code

    m_main.side_effect = ClickShellUncleanExit("Boom!")
    invoke = get_invoke(mock_cli_command)

    with pytest.raises(SystemExit) as exc:
        invoke(Mock(), "mock args")

    assert exc.value.args[0] == expected_error_code


@patch('click.Command.main')
def test_unclean_exit_specific_code(m_main, mock_cli_command):

    expected_error_code = 127

    m_main.side_effect = ClickShellUncleanExit("Boom!", expected_error_code)
    invoke = get_invoke(mock_cli_command)

    with pytest.raises(SystemExit) as exc:
        invoke(Mock(), "mock args")

    assert exc.value.args[0] == expected_error_code


@patch('click.Command.main')
def test_clean_exit(m_main, mock_cli_command):

    m_main.side_effect = ClickShellCleanExit("Boom!")
    invoke = get_invoke(mock_cli_command)

    with pytest.raises(SystemExit) as exc:
        invoke(Mock(), "mock args")

    assert exc.value.args[0] == 0


@patch('click.Command.main')
def test_normal_sys_exit(m_main, mock_cli_command):

    m_main.side_effect = SystemExit("Boom!")
    invoke = get_invoke(mock_cli_command)

    invoke(Mock(), "mock args")


@patch('click.Command.main')
def test_click_exception(m_main, mock_cli_command):

    m_main.side_effect = click.ClickException("Boom!")
    invoke = get_invoke(mock_cli_command)

    invoke(Mock(), "mock args")


@patch('click.Command.main')
def test_click_abort(m_main, mock_cli_command):

    m_main.side_effect = click.Abort("Boom!")
    invoke = get_invoke(mock_cli_command)

    invoke(Mock(), "mock args")


@patch('click.Command.main')
@patch('traceback.print_exception')
def test_regular_exception(m_trace, m_main, mock_cli_command):

    m_main.side_effect = Exception("Boom!")
    invoke = get_invoke(mock_cli_command)

    invoke(Mock(), "mock args")

    m_trace.assert_called_once_with(Exception, m_main.side_effect, None)
