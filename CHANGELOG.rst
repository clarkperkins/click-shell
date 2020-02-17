Version 2.0
-----------

Unreleased

-   Drop support for Python 2.6, 3.3, and 3.4
-   Add support for Python 3.6, 3.7, and 3.8
-   Add support for Click 7
-   Added an ``on_finished`` callback method that will get called when the shell exits. :pr:`16`
-   Added support for a changeable prompt. :issue:`1` :pr:`18`
-   Handle Python installs where ``readline.__doc__`` is None. :issue:`7` :pr:`11`


Version 1.0
-----------

-   Support ``pyreadline`` for Windows. :pr:`5`
-   Fixed a bug where the command name was passed along to the shell. :pr:`4`
