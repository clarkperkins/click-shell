Troubleshooting
===============


Autocomplete
------------

If autocomplete isn't working after installation, you may be missing the ``readline`` module.
Try one of the following depending on your platform:


For macOS / linux (the ``readline`` extra):

.. code-block:: bash

    pip install click-shell[readline]


For Windows / cygwin (the ``windows`` extra):

.. code-block:: bash

    pip install click-shell[windows]
