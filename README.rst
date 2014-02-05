reStructuredText plugin
=======================

This is a little how-to for using the reStructuredText plugin inside 
`GEdit <https://wiki.gnome.org/Apps/Gedit>`_.

.. image:: http://farm3.static.flickr.com/2256/2259897373_d47ecf0983_o_d.png
    :scale: 100
    :alt: reSt Plugin Image
    :align: center
    :target: http://farm3.static.flickr.com/2247/2259897529_aa85f5f540_b.jpg

**Note:** To activate syntax highlighting see `<syntax/README.rst>`_.

Dependencies
------------

- `Python <http://www.python.org/>`_: version >= 3.3
- `Pygments <http://pygments.org/>`_: take the latest version
- `reStructuredText <http://docutils.sourceforge.net/>`_
- `odtwriter <http://www.rexx.com/~dkuhlman/odtwriter.html>`_: a reStructuredText addon to export in OpenOffice format

Installation
------------

- Put ``reST.plugin`` file in GEdit's plugins directory.
  The standard one should be ``~/.local/share/gedit/plugins/``. Alternatively,
  the global directory is something like ``/usr/lib/i386-linux-gnu/gedit/plugins/``.

- Copy the whole ``reST`` folder into the same directory.

You should then obtain something like this: ::

    .../plugins/
            reST.plugin
            reST/
                __init__.py
                makeTable.py
                etc.

Usage
-----

Activate the plugin via *Edit / Preferences / Plugins* and check the checkbox
next to ``reStructuredText Preview``.

The plugin is now activated, and you should have a new panel inside the 
bottom pane named ``reStructuredText Preview``. If you don't see the panel on
the bottom of the editor window make it visible via *View / Bottom Panel*.

Shortcuts
#########

There's only one shortcut for the moment: ``Ctrl+Shift+R``

``Ctrl+Shift+R`` is used to refresh the generated HTML view inside
``reStructuredText Preview`` pane. If there's some selected text, the conversion
will only process the selected portion of the text. If there's no selection, the
entire document is processed. This may be useful for trouble shooting.

Menu
####

The ``Tools`` menu is populated with several options:

- ``reStructuredText Preview`` refreshes the preview pane (same as above)
- ``Create table`` is useful for creating simple reStructuredText tables

**Example:** Enter the two folling lines in gedit, select them and activate
``Create table``: ::

    one,two,tree
    First,Second,Third

The output will be:

=========  ==========  =========
   one        two         tree  
=========  ==========  =========
  First      Second      Third  
=========  ==========  =========

- ``Paste Code`` maybe useful to paste some parts of code using
  `Pygments <http://pygments.org/>`_'s ``sourcecode`` directive.
  Just invoke ``Paste Code`` with something in your clipboard and
  you're done. You'll have to adjust the language afterwards.

- ``--> HTML``, ``--> LaTeX``, ``--> LibreOffice``: are convenient ways to
  export your reStructuredText docs to the given formats with custom *
  stylesheets. If you're not happy with the formatting go ahead and modify
  the stylesheets!
