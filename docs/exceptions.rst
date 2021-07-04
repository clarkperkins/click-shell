Custom Exceptions
=================

click-shell provides two custom exceptions (`ClickShellCleanExit` and `ClickShellUncleanExit`) to allow you terminate the shell under specific conditions.

.. code-block:: python

    import click
    from click_shell import shell
    from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit

    @shell(prompt='my-app > ')
    def my_app():
        print('initializing the application...')

    @my_app.command()
    def cleanexit():
        # Terminates the click-shell and returns exit code 0
        ClickShellCleanExit("I am exiting the shell with an exit status of 0")

    @my_app.command()
    def uncleanexit():
        # Terminates the click-shell and returns exit code 127
        ClickShellUncleanExit("I am exiting the shell with a non-zero exit status", 127)

    # more commands...

    if __name__ == '__main__':
        my_app()
