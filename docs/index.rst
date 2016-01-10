Welcome to click-shell's documentation!
=======================================

click-shell is an extension to `click`_ that easily turns your click app into a shell utility.
It is built on top of the built in python `cmd`_ module, with modifications to make it work
with click.

click-shell is compatible with python versions 2.6, 2.7, 3.3, 3.4, and 3.5.


.. note::

    It should be noted that click-shell **only** alters functionality if no arguments are
    passed on the command line.  Previously if no arguments were passed, the help was displayed.

.. toctree::
   :maxdepth: 2

   install
   usage


.. _click: http://click.pocoo.org/
.. _cmd: https://docs.python.org/2/library/cmd.html
