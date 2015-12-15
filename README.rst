reStructuredText Plugin
=======================

This is a little how-to for using the reStructuredText_ plugin inside gedit_.

.. image:: http://farm3.static.flickr.com/2256/2259897373_d47ecf0983_o_d.png
    :scale: 100
    :alt: reSt Plugin Image
    :align: center
    :target: http://farm3.static.flickr.com/2247/2259897529_aa85f5f540_b.jpg


.. _reStructuredText: http://docutils.sourceforge.net/
.. _gedit: https://wiki.gnome.org/Apps/Gedit

Dependencies
------------

- Python_: version >= 3.3 (-> use `mcepl/reStPlugin`_ for Python 2.x)
- Docutils and Pygments_: ``sudo apt-get install python3-docutils``


.. _mcepl/reStPlugin: https://github.com/mcepl/reStPlugin
.. _Python: http://www.python.org/
.. _Pygments: http://pygments.org/

Installation
------------

- Choose the right source for your version of gedit from the releases_ on
  GitHub.  With ``git`` you can checkout the corresponding tag (e.g.
  ``git checkout gedit-3.8``).

  :gedit-3.8: 3.8 <= gedit < to 3.10
  :gedit-3.10: gedit >= 3.10 (*3.18 has been reported to work fine*)

- Put ``reST.plugin`` file in gedit's plugins directory.  The standard one
  should be ``~/.local/share/gedit/plugins/``.  Alternatively, the global
  directory is something like ``/usr/lib/gedit/plugins/`` or
  ``/usr/lib/<architecture>-linux-gnu/gedit/plugins/``.

- Copy the whole ``reST`` folder into the same directory.

You should then obtain something like this::

    .../plugins/
            reST.plugin
            reST/
                __init__.py
                makeTable.py
                etc.

- Follow the instructions in `<syntax/README.rst>`_ to activate syntax highlighting.
  (Note that recent versions of gedit already ship with this included.  Check
  the language mode drop-down in the footer bar of gedit's editor window.)



.. _releases: https://github.com/bittner/gedit-reST-plugin/releases

Usage
-----

Activate the plugin via *Edit / Preferences / Plugins* and check the checkbox
next to ``reStructuredText Preview``.

The plugin is now activated, and you should have a new panel inside the
bottom pane named ``reStructuredText Preview``. If you don't see the panel on
the bottom of the editor window make it visible via *View / Bottom Panel*.

More Features
#############

Prior versions versions of this plugin had more features (manual reloading
with ``Ctrl+Shift+R``, export to HTML, LaTeX and LibreOffice formats).  See
the `July 4, 2014 version`_ of this README.

If you want these features in again please get your hands dirty and make a
pull request.  The refactored code base of the current version should make
this more easy than ever.  Your contribution is appreciated!


.. _July 4, 2014 version:
    https://github.com/bittner/gedit-reST-plugin/blob/64070843f637aad78f3be4b85478e7e1174a7bca/README.rst#shortcuts


Alternatives
------------

If you're not totally happy with this plugin try the following editors for
quick and free solutions of editing reStructuredText files:

- rsted_ (online reStructuredText editor)
- ReText_ (reStructuredText and MarkDown editor)


.. _rsted: http://rst.ninjs.org/
.. _ReText: https://github.com/retext-project/retext
