Version 2.0
-----------

Released 2020-02-17

- Drop support for Python 2.6, 3.3, and 3.4
- Add support for Python 3.6, 3.7, and 3.8
- Add support for Click 7
- Added an ``on_finished`` callback method that will get called when the shell exits.
  `#16 <https://github.com/clarkperkins/click-shell/pull/16>`_
- Added support for a changeable prompt.
  `#1 <https://github.com/clarkperkins/click-shell/issues/1>`_
  `#18 <https://github.com/clarkperkins/click-shell/pull/18>`_
- Handle Python installs where ``readline.__doc__`` is None.
  `#7 <https://github.com/clarkperkins/click-shell/issues/7>`_
  `#11 <https://github.com/clarkperkins/click-shell/pull/11>`_


Version 1.0
-----------

Released 2016-11-28

- Support ``pyreadline`` for Windows.
  `#5 <https://github.com/clarkperkins/click-shell/pull/5>`_
- Fixed a bug where the command name was passed along to the shell.
  `#4 <https://github.com/clarkperkins/click-shell/pull/4>`_
