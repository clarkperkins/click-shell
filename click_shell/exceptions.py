"""
click_shell.exceptions

Exceptions to allow overrides to the default click_shell error handling.
"""

import sys


class ClickShellCleanExit(Exception):
    """Raised by a command to exit the shell cleanly."""

    def clean_exit(self):       # pylint: disable=no-self-use
        sys.exit(0)


class ClickShellUncleanExit(BaseException):
    """Raised by a command to exit the shell with an error code.

    Set the second exception arg to the error code you wish to use.
    """
    default_error_code = 1

    def unclean_exit(self):
        if len(self.args) > 1:
            sys.exit(self.args[1])
        sys.exit(self.default_error_code)
