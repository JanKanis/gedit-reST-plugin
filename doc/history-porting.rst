=========================
Porting plugin to GEdit 3
=========================

The original version of this plugin was written for GEdit prior to version 3. Unfortunately, version 3 introduced a new API. Old plugins aren't compatible anymore. More infos here:

- http://www.micahcarrick.com/writing-plugins-for-gedit-3-in-python.html
- https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo
- https://developer.gnome.org/gedit/stable/
- https://answers.launchpad.net/ubuntu/+source/gedit/+question/158045
- http://askubuntu.com/questions/185365/what-package-do-i-need-to-install-to-develop-plugins-for-gedit

Known Issues
------------

When you get

1. warnings on the console upon starting ``gedit`` (e.g. on Ubuntu 13.10 Saucy),
#. errors when activating plugins (several ones) in the Preferences dialog,
#. import errors with python/python3, e.g. for ``Gedit``,

it's likely that you have to install package ``gir1.2-gtksource-3.0``::

    sudo apt-get install gir1.2-gtksource-3.0

See also: http://askubuntu.com/questions/369915/warnings-while-launching-gedit-from-the-ubuntu-terminal

Imports to be replaced
----------------------

`__init.py__ <https://github.com/bittner/gedit-reST-plugin/blob/master/reST/__init__.py>`_
    replace ``gtkhtml2`` by ``webkit`` (may need to install Python bindings with: ``sudo apt-get install python-webkit``), import is ``from gi.repository import WebKit``
`makeTable.py <https://github.com/bittner/gedit-reST-plugin/blob/master/reST/makeTable.py>`_
    replace ``cStringIO`` by ``io`` -- **done**
`RegisterPygment.py <https://github.com/bittner/gedit-reST-plugin/blob/master/reST/RegisterPygment.py>`_
    replace ``docutils`` by ``???``

Samples:

- Programming example with Python bindings: http://arstechnica.com/information-technology/2009/07/how-to-build-a-desktop-wysiwyg-editor-with-webkit-and-html-5/

See Also
--------

* `GEdit API documentation <https://developer.gnome.org/gedit/stable/>`_
* `Using the API documentation <http://www.micahcarrick.com/writing-plugins-for-gedit-3-in-python.html#api_documentation>`_
