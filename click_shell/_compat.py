"""
click_shell._compat

Compatibility things for python 2.6
"""

# pylint: disable=unused-import


try:
    from logging import NullHandler
except ImportError:
    import logging

    class NullHandler(logging.Handler):
        """
        Backported from python 2.7
        """
        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None
