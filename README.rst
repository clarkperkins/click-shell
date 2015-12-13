click-shell
===========

click-shell is an extension to `click`_ that easily turns your click app into a shell utility.
It is built on top of the built in python `cmd`_ module, with modifications to make it work
with click.

Usage
-----

Simply add the following to your root level click group:


.. code-block:: python

    import click
    from click_shell import shell

    @click.group(invoke_without_command=True)
    @click.pass_context
    @shell(prompt='my-app > ', intro='Starting my app...')  # Our shell decorator
    def my_app(ctx):
        pass


.. note::

    * You *must* add ``invoke_without_command=True`` to the ``@click.group`` decorator in order for the shell to start up when no command is specified
    * The function *must* be decorated with ``@click.pass_context`` and have a ``ctx`` argument


When run, you should expect an output like so:

.. code-block:: bash

    $ python my_app.py
    Starting my app...
    my-app >


.. _click: http://click.pocoo.org/
.. _cmd: https://docs.python.org/2/library/cmd.html
