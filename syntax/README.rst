Syntax Highlighting for reStructuredText
========================================

In order to enable syntax highlighting for reST in GEdit v3 simply copy the file
``reST.lang`` to the language specs files of GtkSourceView (which seems to manage
highlighting for all langages in GEdit)::

    /usr/share/gtksourceview-3.0/language-specs/

Then you can switch the highlighting manually in the footer bar of GEdit.

Official Repository
-------------------

You can find all language specs officially supported by GtkSourceView, including
the latest version of `rest.lang`_, in the official `GNOME repository`_.
Additional language definitions may be available from the `GNOME Wiki`_.

.. _`rest.lang`: https://git.gnome.org/browse/gtksourceview/tree/data/language-specs/rst.lang
.. _`GNOME repository`: https://git.gnome.org/browse/gtksourceview/tree/data/language-specs/
.. _`GNOME Wiki`: https://wiki.gnome.org/Projects/GtkSourceView/LanguageDefinitions
