.. settings-vial documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Settings Vial - Cloud native settings
=====================================

Quickstart
----------

``$ export MY_APP_TEST_VAR=42``

    >>> from settings_vial imoprt Settings
    >>> settings = Settings(env_preifx="MY_APP_")
    >>> settings.load_env()
    >>> settings.TEST_VAR
    42


API Reference
-------------

In case you are looking for information on a specific function, class, or method.

.. toctree::
   :maxdepth: 2

   api
