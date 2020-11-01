# -*- coding: utf-8 -*-
"""
__init__.py - HTML preview for reStructuredText (.rst) plugin
"""
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

import logging
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')
gi.require_version('Peas', '1.0')
gi.require_version('PeasGtk', '1.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import GObject, Gedit, PeasGtk

from .config import RestructuredtextConfigWidget, Settings
from .restructuredtext import RestructuredtextHtmlContainer


log = logging.getLogger(__name__)


class ReStructuredTextPlugin(GObject.Object, Gedit.WindowActivatable,
                             PeasGtk.Configurable):
    __gtype_name__ = "ReStructuredTextPlugin"

    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        super().__init__()

        self.display_panel = None
        self.html_container = None
        self.handler_id = None

    def do_activate(self):
        panel_name = 'GeditReStructuredTextPanel'
        panel_title = 'reStructuredText'

        self.display_panel = Settings().get_panel(self.window)
        self.html_container = RestructuredtextHtmlContainer(
            self.window, self.display_panel)
        self.html_container.update_view()
        self.html_container.show_now()
        self.display_panel.show_now()

        try:
            self.display_panel.add_titled(self.html_container, panel_name,
                                          panel_title)
        except AttributeError as err:
            log.warning('Falling back to old implementation. Reason: %s', err)
            self.display_panel.add_item(self.html_container, panel_name,
                                        panel_title)
        self.handler_id = self.display_panel.connect(
            "notify::visible-child", self.handle_panel_change)

    def do_deactivate(self):
        self.html_container.clear_view()
        self.display_panel.remove(self.html_container)
        self.display_panel.disconnect(self.handler_id)

    def do_create_configure_widget(self):
        config_widget = RestructuredtextConfigWidget(self)
        return config_widget.configure_widget()

    def do_update_state(self):
        self.html_container.update_view()

    def handle_panel_change(self, panel, prop):
        self.do_update_state()

# ex:et:ts=4:
