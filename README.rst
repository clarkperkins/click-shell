click-shell
===========

|TravisCI| |Sonar| |DocsStatus|

click-shell is an extension to `click`_ that easily turns your click app into a shell utility.
It is built on top of the built in python `cmd`_ module, with modifications to make it work with click.


Features
--------

* Adds a "shell" mode **with command completion** to any click app
* Just a one line change for most click apps


Usage
-----

Simply replace ``@click.group`` with ``@click_shell.shell`` on the root level command:


.. code-block:: python

    import click
    from click_shell import shell

    # @click.group()  # no longer
    @shell(prompt='my-app > ', intro='Starting my app...')
    def my_app():
        pass

    @my_app.command()
    def testcommand():
        click.echo("testcommand is running")

    # more commands

    if __name__ == '__main__':
        my_app()


When run, you should expect an output like so:

.. code-block:: bash

    $ python my_app.py
    Starting my app...
    my-app > testcommand
    testcommand is running
    my-app >


.. note::

    It should be noted that this decorator **only** alters functionality if no arguments are
    passed on the command line.  If you try to run a command directly
    (like ``python my_app.py the_command`` in the above example), your app will function
    identically to how it did before.


For more advanced usage, check out our docs at https://click-shell.readthedocs.io/

.. note::

    Versions of click-shell 3.0.0 and higher no longer support python 2 and click 6.
    If you require python 2 or click 6, please remain on click-shell 2.x.

.. _click: http://click.pocoo.org/
.. _cmd: https://docs.python.org/2/library/cmd.html

.. |TravisCI| image:: https://travis-ci.com/clarkperkins/click-shell.svg?branch=main
    :target: https://travis-ci.com/clarkperkins/click-shell
    :alt: Build status

.. |DocsStatus| image:: https://readthedocs.org/projects/click-shell/badge/?version=latest
    :target: https://click-shell.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |Sonar| image:: https://sonarcloud.io/api/project_badges/measure?project=clarkperkins_click-shell&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=clarkperkins_click-shell
    :alt: Quality Gate Status
