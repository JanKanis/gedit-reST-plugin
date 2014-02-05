#!/usr/bin/env python
# -*- coding: utf-8 -*-

# restPlugin - HTML preview of reSt formatted text in gedit
#
# Copyright (C) 2007 - Christophe Kibleur
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from docutils.core import publish_parts
from gi.repository import Gedit, GObject, Gtk, WebKit
from gettext import gettext as _
#from makeTable import toRSTtable
#import RegisterPygment
import os


## I'm not satisfied with that
restpluginDir = os.path.dirname(os.path.abspath(__file__))
css = os.path.join(restpluginDir, 'restmain.css')
styles = open(css, 'r')

START_HTML = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Language" content="English" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style type="text/css">
        %s
    </style>
</head>
<body>""" % (styles.read())

styles.close()

END_HTML = """</body>
</html>
"""

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <separator/>
      <placeholder name="ToolsOps_6">
        <menuitem name="preview" action="preview"/>
      </placeholder>
      <placeholder name="ToolsOps_6">
        <menuitem name="table" action="table"/>
      </placeholder>
      <placeholder name="ToolsOps_6">
        <menuitem name="sourcecode" action="sourcecode"/>
      </placeholder>
      <placeholder name="ToolsOps_6">
        <menuitem name="--> HTML" action="--> HTML"/>
      </placeholder>
      <placeholder name="ToolsOps_6">
        <menuitem name="--> LaTeX" action="--> LaTeX"/>
      </placeholder>
      <placeholder name="ToolsOps_6">
        <menuitem name="--> LibreOffice" action="--> LibreOffice"/>
      </placeholder>
      <separator/>
    </menu>
  </menubar>
</ui>
"""


class restPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "reStructuredTextPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        ## TODO : Maybe have to check the filetype ?

        # Store data in the window object
        windowdata = dict()
        self.window.reStPreviewData = windowdata

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_property("hscrollbar-policy",
                                     Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_property("vscrollbar-policy",
                                     Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_property("shadow-type",
                                     Gtk.ShadowType.IN)

        html_view = WebKit.WebView()
        html_view.load_string("%s\n<p>reStructuredText Viewer</p>\n%s" %
                              (START_HTML, END_HTML), 'text/html', 'utf8', '')

        #scrolled_window.set_hadjustment(html_view.get_hadjustment())
        #scrolled_window.set_vadjustment(html_view.get_vadjustment())
        scrolled_window.add(html_view)
        scrolled_window.show_all()

        bottom = self.window.get_bottom_panel()
        image = Gtk.Image()
        image.set_from_icon_name("gnome-mime-text-html", Gtk.IconSize.MENU)
        bottom.add_item(scrolled_window, "rest-preview", "reStructuredText Preview", image)
        windowdata["bottom_panel"] = scrolled_window
        windowdata["html_doc"] = html_view

        manager = self.window.get_ui_manager()

        ## Added later
        self._action_group = Gtk.ActionGroup("reStPluginActions")
        self._action_group.add_actions([("preview", None, _("reStructuredText Preview"),
                                         "<Control><Shift>R", _("reStructuredText Preview"),
                                         self.on_update_preview),
                                        ("table", None, _("Create table"),
                                         None, _("Create a reStructuredText table"),
                                         self.on_create_table),
                                        ("sourcecode", None, _("Paste Code"),
                                         None, _("Paste source code"),
                                         self.on_paste_code),
                                        ("--> HTML", None, _("--> HTML"),
                                         None, _("Save as HTML document"),
                                         self.on_html),
                                        ("--> LaTeX", None, _("--> LaTeX"),
                                         None, _("Save as LaTeX document"),
                                         self.on_latex),
                                        ("--> LibreOffice", None, _("--> LibreOffice"),
                                         None, _("Save as LibreOffice ODF"),
                                         self.on_libreoffice),
        ])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def do_deactivate(self):
        # Retrieve the data of the window object
        windowdata = self.window.reStPreviewData

        # Remove the menu action
        if 'ui_id' in windowdata:
            manager = self.window.get_ui_manager()
            manager.remove_ui(windowdata["ui_id"])
            manager.remove_action_group(windowdata["action_group"])

        # Remove the bottom panel
        bottom = self.window.get_bottom_panel()
        bottom.remove_item(windowdata["bottom_panel"])

    def getSelection(self):
        view = self.window.get_active_view()
        if not view:
            return

        doc = view.get_buffer()

        start = doc.get_start_iter()
        end = doc.get_end_iter()

        if doc.get_selection_bounds():
            start = doc.get_iter_at_mark(doc.get_insert())
            end = doc.get_iter_at_mark(doc.get_selection_bound())

        text = doc.get_text(start, end)

    # Menu activate handlers
    def on_update_preview(self, window):
        # Retrieve the data of the window object
        windowdata = self.window.reStPreviewData

        view = self.window.get_active_view()
        if not view:
            return

        doc = view.get_buffer()

        start = doc.get_start_iter()
        end = doc.get_end_iter()

        if doc.get_selection_bounds():
            start = doc.get_iter_at_mark(doc.get_insert())
            end = doc.get_iter_at_mark(doc.get_selection_bound())

        text = doc.get_text(start, end, False)
        html = publish_parts(text, writer_name="html")["html_body"]

        p = windowdata["bottom_panel"].get_placement()

        html_doc = windowdata["html_doc"]
        html_doc.load_string("%s\n%s\n%s" % (START_HTML, html, END_HTML),
                             'text/html', 'utf8', '')

        windowdata["bottom_panel"].set_placement(p)

    def on_latex(self, action):
        command = 'python3 %s/to_tex.py "%s.rst" "%s.tex"'
        doc = self.window.get_active_document()
        filename = doc.get_uri_for_display()[:-4]
        os.system(command % (restpluginDir, filename, filename))

    def on_html(self, action):
        command = 'python3 %s/to_html.py --stylesheet=%s/restmain.css --language=en "%s.rst" "%s.html"'
        doc = self.window.get_active_document()
        filename = doc.get_uri_for_display()[:-4]
        os.system(command % (restpluginDir, restpluginDir, filename, filename))

    def on_libreoffice(self, action):
        command = 'python3 %s/to_odt.py --add-syntax-highlighting --stylesheet=%s/default.odt "%s.rst" "%s.odt"'
        doc = self.window.get_active_document()
        filename = doc.get_uri_for_display()[:-4]
        os.system(command % (restpluginDir, restpluginDir, filename, filename))

    def on_paste_code(self, action):
        doc = self.window.get_active_document()

        if not doc:
            return

        lines = Gtk.clipboard_get().wait_for_text().split('\n')
        to_copy = "\n".join([line for line in lines[1:]])
        doc.insert_at_cursor('..sourcecode:: ChoosenLanguage\n\n    %s\n' % lines[0])
        doc.insert_at_cursor(to_copy + '\n\n')

    def on_create_table(self, action):
        view = self.window.get_active_view()

        if not view:
            return

        indent = view.get_indent()

        doc = view.get_buffer()
        #print('language=%s' %s doc.get_language())

        start = doc.get_start_iter()
        end = doc.get_end_iter()

        if doc.get_selection_bounds():
            start = doc.get_iter_at_mark(doc.get_insert())
            end = doc.get_iter_at_mark(doc.get_selection_bound())

        text = doc.get_text(start, end)
        doc.delete(start, end)

        lines = text.split("\n")
        labels = lines[0].split(',')
        rows = [row.strip().split(',') for row in lines[1:]]

        doc.insert_at_cursor(toRSTtable([labels] + rows))
