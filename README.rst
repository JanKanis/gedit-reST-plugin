reStructuredText Plugin
=======================

This is a little how-to for using the reStructuredText plugin inside gedit_.

.. image:: http://farm3.static.flickr.com/2256/2259897373_d47ecf0983_o_d.png
    :scale: 100
    :alt: reSt Plugin Image
    :align: center
    :target: http://farm3.static.flickr.com/2247/2259897529_aa85f5f540_b.jpg


.. _gedit: https://wiki.gnome.org/Apps/Gedit

Dependencies
------------

- Python_: version >= 3.3 (-> use `mcepl/reStPlugin`_ for Python 2.x)
- Pygments_: take the latest version
- reStructuredText_
- odtwriter_: a reStructuredText addon to export in LibreOffice format


.. _mcepl/reStPlugin: https://github.com/mcepl/reStPlugin
.. _Python: http://www.python.org/
.. _Pygments: http://pygments.org/
.. _reStructuredText: http://docutils.sourceforge.net/
.. _odtwriter: http://www.rexx.com/~dkuhlman/odtwriter.html

Installation
------------

- Choose the right source for your version of gedit from the releases_ on
  GitHub.  With ``git`` you can checkout the corresponding tag (e.g.
  ``git checkout gedit-3.12``).

  :gedit-3.8: 3.8 <= gedit < to 3.12
  :gedit-3.14: gedit >= 3.12

- Put ``reST.plugin`` file in gedit's plugins directory.
  The standard one should be ``~/.local/share/gedit/plugins/``. Alternatively,
  the global directory is something like ``/usr/lib/gedit/plugins/`` or
  ``/usr/lib/<architecture>-linux-gnu/gedit/plugins/``.

- Copy the whole ``reST`` folder into the same directory.

You should then obtain something like this: ::

    .../plugins/
            reST.plugin
            reST/
                __init__.py
                makeTable.py
                etc.

- Follow the instructions in `<syntax/README.rst>`_ to activate syntax highlighting.


.. _releases: https://github.com/bittner/gedit-reST-plugin/releases

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

**Example:** Enter the two following lines in gedit, select them and activate
``Create table``::

    one,two,tree
    First,Second,Third

The output will be:

=========  ==========  =========
   one        two         tree
=========  ==========  =========
  First      Second      Third
=========  ==========  =========

- ``Paste Code`` maybe useful to paste some parts of code using the
  ``sourcecode`` directive of Pygments_.
  Just invoke ``Paste Code`` with something in your clipboard and you're done.
  You'll have to adjust the language afterwards.

- ``--> HTML``, ``--> LaTeX``, ``--> LibreOffice``: are convenient ways to
  export your reStructuredText docs to the given formats with custom *
  stylesheets. If you're not happy with the formatting go ahead and modify
  the stylesheets!

Alternatives
------------

If you're not totally happy with this plugin try the following editors for
quick and free solutions of editing reStructuredText files:

- rsted_ (online reStructuredText editor)
- ReText_ (reStructuredText and MarkDown editor)


.. _rsted: http://rst.ninjs.org/
.. _ReText: https://github.com/retext-project/retext
