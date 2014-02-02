reStructuredText plugin
=======================

This is a little how-to for using the reStructuredText plugin inside 
`GEdit <http://www.gnome.org/projects/gedit/>`_ .

.. image:: http://farm3.static.flickr.com/2256/2259897373_d47ecf0983_o_d.png
    :scale: 100
    :alt: reSt Plugin Image
    :align: center
    :target: http://farm3.static.flickr.com/2247/2259897529_aa85f5f540_b.jpg


Dépendancies
------------

- `Python <http://www.python.org/>`_ : version >= 2.5;
- `Pygments <http://pygments.org/>`_ : take the latest version;
- `reStructuredText <http://docutils.sourceforge.net/>`_ ;
- `odtwriter <http://www.rexx.com/~dkuhlman/odtwriter.html>`_ : a reStructuredText addon to export in OpenOffice format.

Installation
------------
Unpack the zip file where you wanted to then :

- Put ``reSt.gedit-plugin`` file in Gedit's plugins directory.
  Mine is (under Ubuntu Gutsy): ``/home/kib/.gnome2/gedit/plugins``

- Copy/Paste the ``reStPlugin`` folder inside ``/home/kib/.gnome2/gedit/plugins``.

Readme.rst and Readme.odt are just help files, you can do whatever you want with them.

You should then obtain something like this : ::

    .../plugins/
            reSt.gedit-plugin
            reStPlugin/
                __init__.py
                makeTable.py
                etc.

Using
-----

Activate the plugin via Edit/Préférences/Plugins and turn the
``reStructuredText plugin`` box on.

The plugin is now activated, and you should have a new panel inside the 
bottom pane named ``reSt Preview``.

Shortcuts
#########

There's only one shortcut for the moment, maybe I'll create some others in the
future.

``Ctrl+Maj+R`` : is used to refresh the generated HTML view inside 
``reSt Preview`` pane. If there's some selected text, the conversion process
will only apply on it. If there's no selection, the entire document is 
processed. It may be usefull for testing.

Menu
####

The ``Tools`` menu is populated with several options :

- ``reSt Preview`` is the same as the above;
- ``Create table`` is usefull for creating simple reStructuredText tables.

Example : Enter the two folling lines in gedit, select them and activate 
``Create table`` : ::

    one,two,tree
    First,Second,Third

The output will be :

=========  ==========  =========
   one        two         tree  
=========  ==========  =========
  First      Second      Third  
=========  ==========  =========

- ``Paste Code`` maybe usefull to paste some parts of code using 
  `Pygments <http://pygments.org/>`_'s ``sourcecode`` directive.
  Just invoque ``Paste Code`` with something in your clipboard and
  you're done. You'll have to adjust the language afterwards.

- ``--> HTML``, ``--> LaTeX``, ``--> OpenOffice``: are convenient ways to
  export your reStructuredText docs to the given formats with custom *
  stylesheets. You're free to modify them, even to propose your own because
  I'm not a CSS ace :)

Hoping it helps you, to contact me, drop me a message here : kib2 at free.fr

See you,

Kib.
