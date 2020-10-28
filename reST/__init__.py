# -*- coding: utf-8 -*-

# __init__.py - HTML preview for reStructuredText (.rst) plugin
#
# Copyright (C) 2014-2018 - Peter Bittner
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

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')
gi.require_version('Peas', '1.0')
gi.require_version('PeasGtk', '1.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import GObject, Gedit, PeasGtk

from .config import RestructuredtextConfigWidget, Settings
from .restructuredtext import RestructuredtextHtmlPanel


class ReStructuredTextPlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "ReStructuredTextPlugin"

    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

        self._panel = None

    def do_activate(self):
        panel_name = 'GeditReStructuredTextPanel'
        panel_title = 'reStructuredText Preview'

        self.container = Settings().get_panel(self.window)
        self._panel = RestructuredtextHtmlPanel(self.window, self.container)
        self._panel.update_view()
        self._panel.show()

        try:
            self.container.add_titled(self._panel, panel_name, panel_title)
        except AttributeError as err:
            print('Falling back to old implementation. Reason: %s' % err)
            self.container.add_item(self._panel, panel_name, panel_title)
        self.handler_id = self.container.connect(
            "notify::visible-child", self.handle_panel_change)

    def do_deactivate(self):
        self._panel.clear_view()
        self.container.remove(self._panel)
        self.container.disconnect(self.handler_id)

    def do_create_configure_widget(self):
        data_dir = self.plugin_info.get_data_dir()
        config_widget = RestructuredtextConfigWidget(data_dir)
        return config_widget.configure_widget()

    def do_update_state(self):
        self._panel.update_view()

    def handle_panel_change(self, panel, prop):
        self.do_update_state()

# ex:et:ts=4:
