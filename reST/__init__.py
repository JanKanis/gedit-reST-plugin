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

    def do_activate(self):
        log.debug("panel index: %s", Settings.get().get_panel_index())
        self.display_panel = self.get_panel()
        self.html_container = RestructuredtextHtmlContainer(
            self.window, self.display_panel)
        self.add_container_to_panel()
        self.html_container.show_now()
        self.display_panel.show_now()
        self.html_container.update_view()

        Settings.get().connect(self.on_panel_setting_change)

    def get_panel(self):
        panel_name = Settings.get().get_panel()
        if panel_name == 'side':
            return self.window.get_side_panel()
        elif panel_name == 'bottom':
            return self.window.get_bottom_panel()
        else:
            raise AssertionError(f"got unsupported panel name {panel_name}, "
                                 f"expecting 'side' or 'bottom'")

    def add_container_to_panel(self):
        panel_name = 'GeditReStructuredTextPanel'
        panel_title = 'reStructuredText'

        try:
            self.display_panel.add_titled(self.html_container, panel_name,
                                          panel_title)
        except AttributeError as err:
            log.warning('Falling back to old implementation. Reason: %s', err)
            self.display_panel.add_item(self.html_container, panel_name,
                                        panel_title)
        self.html_container.set_panel(self.display_panel)
        self.display_panel.connect("notify::visible-child",
                                   self.do_update_state)

    def remove_container_from_panel(self):
        self.display_panel.disconnect_by_func(self.do_update_state)
        self.display_panel.remove(self.html_container)

    def do_deactivate(self):
        self.html_container.clear_view()
        self.display_panel.remove(self.html_container)
        self.display_panel.disconnect_by_func(self.do_update_state)
        Settings.get().disconnect_by_func(self.on_panel_setting_change)

    def do_create_configure_widget(self):
        config_widget = RestructuredtextConfigWidget(self)
        return config_widget.configure_widget()

    def do_update_state(self, *ignored):
        self.html_container.update_view()

    def on_panel_setting_change(self, settings, setting):
        new_panel = self.get_panel()
        if new_panel is self.display_panel:
            return
        log.debug("Panel changed to '%s'", Settings.get().get_panel())

        self.remove_container_from_panel()

        self.display_panel = new_panel
        self.add_container_to_panel()
        self.do_update_state()

# ex:et:ts=4:
