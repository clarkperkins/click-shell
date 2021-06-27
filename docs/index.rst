Welcome to click-shell's documentation!
=======================================

click-shell is an extension to `click`_ that easily turns your click app into a shell utility.
It is built on top of the built in python `cmd`_ module, with modifications to make it work with click.

click-shell is compatible with python versions 3.6, 3.7, 3.8, and 3.9.


Features
--------

* Adds a "shell" mode **with command completion** to any click app
* Just a one line change for most click apps


.. note::

    It should be noted that click-shell **only** alters functionality if no arguments are
    passed on the command line.  Previously if no arguments were passed, the help was displayed.

.. toctree::
   :maxdepth: 2

   install
   usage
   changelog
   troubleshooting


.. _click: https://click.palletsprojects.com/
.. _cmd: https://docs.python.org/3/library/cmd.html
