Usage
=====

There are 2 main ways to utilize click-shell: the decorator and the factory method.

Decorator
---------

The easiest way to get going with click-shell is with the click style decorator:

.. code-block:: python

    import click
    from click_shell import shell

    @click.group(invoke_without_command=True)
    @click.pass_context
    @shell(prompt='my-app > ', intro='Starting my app...')  # The shell decorator
    def my_app(ctx):
        pass


.. note::

   - You *must* add ``invoke_without_command=True`` to the ``@click.group`` decorator in order for
     the shell to start up when no command is specified
   - The function *must* be decorated with ``@click.pass_context`` and have a ``ctx`` argument


When run, you should expect an output like so:

.. code-block:: bash

    $ python my_app.py
    Starting my app...
    my-app >


Factory Method
--------------

If you'd rather not use decorators (or can't for some reason), you can manually create a shell
object and start it up:


.. code-block:: python

    import click
    from click_shell import make_click_shell

    @click.group()
    @click.pass_context
    def my_app(ctx):
        pass



    # Somewhere else in your code (as long as you have access to the root level Context object)

    shell = make_click_shell(ctx, prompt='my-app > ', intro='Starting my app...')
    shell.cmdloop()
