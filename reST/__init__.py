# -*- coding: utf-8 -*-

# __init__.py - HTML preview for reStructuredText (.rst) plugin
#
# Copyright (C) 2015 - Peter Bittner
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
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject, Gtk, Gedit, Peas, PeasGtk, WebKit

from .restructuredtext import RestructuredtextHtmlPanel
# from .config import RestructuredtextConfigWidget


class ReStructuredTextPlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "ReStructuredTextPlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.html_window = None

    def do_activate(self):
        self.html_window = RestructuredtextHtmlPanel()
        self.html_window.update_view()
        bottom = self.window.get_bottom_panel()
        bottom.add_titled(self.html_window, "GeditReStructuredTextPanel", _('reStructuredText Preview'))

    def do_deactivate(self):
        self.html_window.clear_view()
        bottom = self.window.get_bottom_panel()
        bottom.remove(self.html_window)

    def do_update_state(self):
        pass

#    def do_create_configure_widget(self):
#        config_widget = PythonConsoleConfigWidget(self.plugin_info.get_data_dir())
#
#        return config_widget.configure_widget()

# ex:et:ts=4:
