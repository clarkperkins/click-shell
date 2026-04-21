import re
from click_shell.cmd import ClickCmd

def test_fix_prompt_no_readline():
    # Simulate no readline
    import click_shell.cmd
    original_readline = click_shell.cmd.readline
    click_shell.cmd.readline = None
    try:
        cmd = ClickCmd()
        prompt = '\x1b[34mmy-shell> \x1b[0m'
        assert cmd._fix_prompt(prompt) == prompt
    finally:
        click_shell.cmd.readline = original_readline

def test_fix_prompt_with_ansi():
    # We need to make sure readline is "present" for the test
    import click_shell.cmd
    original_readline = click_shell.cmd.readline
    if click_shell.cmd.readline is None:
        # mock it
        class MockReadline:
            __name__ = 'readline'
        click_shell.cmd.readline = MockReadline()
    
    try:
        cmd = ClickCmd()
        prompt = '\x1b[34mmy-shell> \x1b[0m'
        fixed = cmd._fix_prompt(prompt)
        assert fixed == '\x01\x1b[34m\x02my-shell>\x01\x1b[0m\x02 '
    finally:
        click_shell.cmd.readline = original_readline

def test_fix_prompt_already_wrapped():
    import click_shell.cmd
    original_readline = click_shell.cmd.readline
    if click_shell.cmd.readline is None:
        class MockReadline:
            __name__ = 'readline'
        click_shell.cmd.readline = MockReadline()
    
    try:
        cmd = ClickCmd()
        prompt = '\x01\x1b[34m\x02my-shell> \x01\x1b[0m\x02'
        fixed = cmd._fix_prompt(prompt)
        assert fixed == prompt
    finally:
        click_shell.cmd.readline = original_readline

def test_fix_prompt_pyreadline():
    import click_shell.cmd
    original_readline = click_shell.cmd.readline
    
    # Mock pyreadline
    class MockPyReadline:
        __name__ = 'pyreadline'
    click_shell.cmd.readline = MockPyReadline()
    
    try:
        cmd = ClickCmd()
        prompt = '\x1b[34mmy-shell> \x1b[0m'
        assert cmd._fix_prompt(prompt) == prompt
    finally:
        click_shell.cmd.readline = original_readline

def test_fix_prompt_trailing_space():
    import click_shell.cmd
    original_readline = click_shell.cmd.readline
    if click_shell.cmd.readline is None:
        class MockReadline:
            __name__ = 'readline'
        click_shell.cmd.readline = MockReadline()
    
    try:
        cmd = ClickCmd()
        # click.style typically places the reset code at the very end
        prompt = '\x1b[34mmy-shell> \x1b[0m'
        fixed = cmd._fix_prompt(prompt)
        # the space should be moved outside the \x02 wrapper
        assert fixed == '\x01\x1b[34m\x02my-shell>\x01\x1b[0m\x02 '
        
        # Test with multiple trailing spaces
        prompt2 = '\x1b[34mmy-shell>   \x1b[0m'
        fixed2 = cmd._fix_prompt(prompt2)
        assert fixed2 == '\x01\x1b[34m\x02my-shell>\x01\x1b[0m\x02   '
    finally:
        click_shell.cmd.readline = original_readline
