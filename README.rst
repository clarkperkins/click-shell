click-shell
===========

|TravisCI| |DocsStatus|

click-shell is an extension to `click`_ that easily turns your click app into a shell utility.
It is built on top of the built in python `cmd`_ module, with modifications to make it work
with click.

Usage
-----

Simply replace ``@click.group`` with ``@click_shell.shell`` on the root level command:


.. code-block:: python

    from click_shell import shell

    # @click.group()  # no longer
    @shell(prompt='my-app > ', intro='Starting my app...')
    def my_app(ctx):
        pass

    @my_app.command()
    def the_command():
        print 'the_command is running'

    ...


When run, you should expect an output like so:

.. code-block:: bash

    $ python my_app.py
    Starting my app...
    my-app >


For more advanced usage, check out our docs at http://click-shell.readthedocs.org/

.. _click: http://click.pocoo.org/
.. _cmd: https://docs.python.org/2/library/cmd.html

.. |TravisCI| image:: https://travis-ci.org/clarkperkins/click-shell.svg?branch=master
   :target: https://travis-ci.org/clarkperkins/click-shell
   :alt: Build status

.. |DocsStatus| image:: https://readthedocs.org/projects/click-shell/badge/?version=latest
   :target: http://click-shell.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status
