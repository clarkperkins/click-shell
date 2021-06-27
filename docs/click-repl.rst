Differences with click-repl
===========================

`Click-repl`_ is another Click extension that provides a feature similar
to click-shell. This page lists the main differences between the two
extensions.


Click-shell sets the shell as the default subcommand
----------------------------------------------------

With click-shell, the interactive shell is automatically started if the
Click application is invoked without an explicit subcommand.

By contrast, click-repl adds a new subcommand to start the shell (named
``repl`` by default), but that command is *not* used by default. If the
program is invoked without a subcommand, the help message is displayed
(as with standard Click). The user has to explicitly invoke the ``repl``
command to get the interactive shell.


Click-shell calls the root function only once
---------------------------------------------

This is possibly the most important difference, depending on how your
Click application is designed.

To understand it, consider the following minimal example with
click-shell:

.. code-block:: python

    import click
    from click_shell import shell

    @shell(prompt='my-app > ')
    def my_app():
        print('initializing the application...')

    @my_app.command()
    def testcommand():
        print('testcommand is running')

    # more commands...

    if __name__ == '__main__':
        my_app()

The code inside the ``my_app`` function will always be called only once,
just before the interactive shell is started:

.. code-block:: bash

    $ python my_app.py
    initializing the application...
    my-app > testcommand
    testcommand is running
    my-app > testcommand
    testcommand is running
    my-app >


By contrast, with the equivalent code using click-repl:

.. code-block:: python

    import click
    from click_repl import register_repl

    @click.group()
    def my_app():
        print('initializing the application...')

    @my_app.command()
    def testcommand():
        print('testcommand is running')

    # more commands...

    if __name__ == '__main__':
        register_repl(my_app)
        my_app()

The code inside the ``my_app`` function will be executed when the
application is started *and* before the invocation of any subcommand
from the interactive shell:

.. code-block:: bash

    $ python my_app.py repl
    initializing the application...
    > testcommand
    initializing the application...
    testcommand is running
    > testcommand
    initializing the application...
    testcommand is running
    >

Obviously that difference in behaviour does not matter if the "root"
function of your Click app (``my_app`` in those examples) does nothing.
But if that function does anything meaningful (such as performing some
initialization steps, reading a configuration file, etc.), then you must
be aware of that difference. With click-repl, you need to make sure it
is acceptable for the code in your root function to be called repeatedly
over the lifetime of the application.


Click-shell has no shell escape
-------------------------------

The interactive shell created by click-repl allows the user to invoke
commands from the underlying system shell in addition to the commands
from the application itself, by prefixing them with ``!``.

Click-shell has no such feature.

.. _click-repl: https://github.com/click-contrib/click-repl
