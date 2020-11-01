reStructuredText plugin
=======================

This is a little how-to for using the reStructuredText plugin inside
`gedit <https://wiki.gnome.org/Apps/Gedit>`_.

.. image:: http://farm3.static.flickr.com/2256/2259897373_d47ecf0983_o_d.png
    :scale: 100
    :alt: reSt Plugin Image
    :align: center
    :target: http://farm3.static.flickr.com/2247/2259897529_aa85f5f540_b.jpg

**Note:** Syntax highlighting works out-of-the-box with any new version of
gedit. For older versions see `<syntax/README.rst>`_.

Dependencies
------------

- `Python <http://www.python.org/>`_: version >= 3.3
- `Pygments <http://pygments.org/>`_: take the latest version
- `reStructuredText <http://docutils.sourceforge.net/>`_
- `odtwriter <http://www.rexx.com/~dkuhlman/odtwriter.html>`_: a reStructuredText addon to export in OpenOffice format

Installation
------------

- Put ``reST.plugin`` file in gedit's plugins directory.
  The standard one should be ``~/.local/share/gedit/plugins/``. Alternatively,
  the global directory is something like ``/usr/lib/i386-linux-gnu/gedit/plugins/``.

- Copy the whole ``reST`` folder into the same directory.

You should then obtain something like this: ::

    .../plugins/
            reST.plugin
            reST/
                schemas/
                  gschemas.compiled
                  org.gnome.gedit.plug...
                __init__.py
                config.py
                restructuredtext.py
                ...

Usage
-----

Activate the plugin via *Edit > Preferences > Plugins* and check the checkbox
next to **reStructuredText Preview**. Optionally, you can also choose whether
you want the preview displayed in the bottom or the side panel.

The plugin is now activated, and you should have a new tab inside the
bottom panel named *reStructuredText*. If you don't see the panel on
the bottom of the editor window make it visible via *View > Bottom Panel*.
If you use the side panel operate the drop-down selector on top of it
to switch between *Documents* view and *reStructuredText*.

Features
########

:Selection:
    You can select some text to render only the selected portion of the
    document. If there's no selection, the entire document is processed.

    You may find this useful for trouble-shooting markup directives.

Broken Features
###############

➜ *Please contribute to bring these features back in the new implementation!*

:Reload:
    It used to be possible to force re-rendering of the reStructuredText
    document using the <kbd>Ctrl</kbd>+<kbd>R</kbd> keyboard shortcut.

:Tools:
    The *Tools* menu used to be populated with several options:

    - *reStructuredText Preview* refreshes the preview pane
      (<kbd>Ctrl</kbd>+<kbd>R</kbd>)

    - *Create table* is useful for creating simple reStructuredText tables

      **Example:** Enter the two following lines in gedit, select them and
      trigger *Create table*:

      .. code-block:: reStructuredText

        one,two,tree
        First,Second,Third

      The output will be:

      .. code-block:: reStructuredText

        =========  ==========  =========
          one        two         tree
        =========  ==========  =========
          First      Second      Third
        =========  ==========  =========

    - *Paste Code* maybe useful to paste some parts of code using
      `Pygments <http://pygments.org/>`_'s ``sourcecode`` directive.
      Just invoke *Paste Code* with something in your clipboard and
      you're done. You'll have to adjust the language afterwards.

    - *➜ HTML*, *➜ LaTeX*, *➜ LibreOffice*: are convenient ways to export
      your reStructuredText docs to the given formats with custom
      stylesheets. If you're not happy with the formatting go ahead and
      modify the stylesheets yourself.
