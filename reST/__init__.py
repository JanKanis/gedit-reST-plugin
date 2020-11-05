# -*- coding: utf-8 -*-
"""
HTML preview for reStructuredText (.rst) plugin
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

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ReStructuredTextPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ReStructuredTextPlugin"

    window = GObject.Property(type=Gedit.Window)
    instance = None

    def __init__(self):
        super().__init__()

        if ReStructuredTextPlugin.instance is not None:
            log.warning("A new ReStructuredTextPlugin instance was "
                        "instantiated while one already exists. "
                        "Existing: %s; New: %s",
                        ReStructuredTextPlugin.instance, self)
        ReStructuredTextPlugin.instance = self

        self.display_panel = None
        self.html_container = None

    def do_activate(self):
        log.debug("panel: %s", Settings.get().get_panel_name())
        self.display_panel = self.get_panel()
        self.html_container = RestructuredtextHtmlContainer(
            self.window, self.display_panel)
        self.add_container_to_panel()
        self.html_container.show()
        self.html_container.update_view()

        Settings.get().connect(self.on_panel_setting_change)

    def get_panel(self):
        panels = {
            'bottom-panel': self.window.get_bottom_panel,
            'side-panel': self.window.get_side_panel,
        }
        panel_name = Settings.get().get_panel_name()
        try:
            return panels[panel_name]()
        except KeyError:
            raise RuntimeError("Got unsupported panel name %s, "
                               "expected 'side' or 'bottom'" % panel_name)

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
        self.display_panel.connect("notify::visible", self.do_update_state)
        self.display_panel.connect("notify::visible-child",
                                   self.do_update_state)

    def remove_container_from_panel(self):
        self.display_panel.disconnect_by_func(self.do_update_state)
        self.display_panel.disconnect_by_func(self.do_update_state)
        self.display_panel.remove(self.html_container)

    def do_deactivate(self):
        self.html_container.clear_view()
        self.display_panel.remove(self.html_container)
        self.display_panel.disconnect_by_func(self.do_update_state)
        Settings.get().disconnect_by_func(self.on_panel_setting_change)
        ReStructuredTextPlugin.instance = None

    def do_update_state(self, *ignored):
        self.html_container.update_view()

    def on_panel_setting_change(self, settings, setting):
        new_panel = self.get_panel()
        if new_panel is self.display_panel:
            return
        log.debug("Panel changed to '%s'", Settings.get().get_panel_name())

        self.remove_container_from_panel()

        self.display_panel = new_panel
        self.add_container_to_panel()
        self.do_update_state()

    def force_show_preview(self):
        self.display_panel.set_visible(True)
        self.display_panel.set_visible_child(self.html_container)


class RestructuredTextPluginConfig(GObject.Object, PeasGtk.Configurable):
    def __init__(self):
        super().__init__()

    def do_create_configure_widget(self):
        plugin_object = ReStructuredTextPlugin.instance
        if plugin_object is None:
            log.error("No plugin object instance found even though the plugin "
                      "configuration panel is being opened")
        config_widget = RestructuredtextConfigWidget(plugin_object)
        return config_widget.configure_widget()

# ex:et:ts=4:
