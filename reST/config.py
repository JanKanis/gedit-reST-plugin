# -*- coding: utf-8 -*-
"""
Preferences dialog and configuration settings
"""
# Copyright (C) 2020 - Peter Bittner and contributors
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

import os
import logging

from gi.repository import Gio, Gtk

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
REST_KEY_BASE = 'com.github.bittner.gedit-rest-plugin'
REST_KEY_PREVIEW_PANEL = 'preview-panel'
REST_PREVIEW_PANELS = ['bottom-panel', 'side-panel']

log = logging.getLogger(__name__)


class Settings:
    """
    Gtk settings schema and settings wrapper.
    """

    _instance = None

    @classmethod
    def get(cls):
        """
        Return the singleton instance.
        """
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance

    def __init__(self):
        """
        Read the compiled settings schema from disk.
        """
        schemas_path = os.path.join(BASE_PATH, 'schemas')
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            schemas_path, Gio.SettingsSchemaSource.get_default(), False)
        schema = schema_source.lookup(REST_KEY_BASE, False)
        self.settings = Gio.Settings.new_full(schema, None, None)

    def get_panel_name(self):
        return self.settings.get_string(REST_KEY_PREVIEW_PANEL)

    def set_panel(self, name):
        self.settings.set_string(REST_KEY_PREVIEW_PANEL, name)

    def connect(self, callback, *args):
        return self.settings.connect("changed::%s" % REST_KEY_PREVIEW_PANEL,
                                     callback, *args)

    def disconnect_by_func(self, callback_func):
        self.settings.disconnect_by_func(callback_func)


class RestructuredtextConfigWidget:
    """
    Preferences dialog factory.
    """

    def __init__(self, plugin_instance):
        self._plugin_instance = plugin_instance
        datadir = plugin_instance.plugin_info.get_data_dir()
        self._ui_path = os.path.join(datadir, 'config.ui')
        self._ui = Gtk.Builder()
        self._settings = Settings.get()
        self._last_choice = None

    def configure_widget(self):
        self._ui.add_from_file(self._ui_path)

        configured_panel = self._settings.get_panel_name()

        for panel_name in REST_PREVIEW_PANELS:
            radiobutton = self._ui.get_object(panel_name)
            radiobutton.connect('toggled', self.on_button_toggled, panel_name)
            radiobutton.set_active(configured_panel == panel_name)
            if configured_panel == panel_name:
                self._last_choice = panel_name

        widget = self._ui.get_object('restructuredtext_preferences')
        return widget

    def on_button_toggled(self, radiobutton, panel_name):
        if radiobutton.get_active():
            self._settings.set_panel(panel_name)

            # preview container has been moved to the new panel at this point
            if self._last_choice != panel_name:
                self._plugin_instance.force_show_preview()
                self._plugin_instance.do_update_state()
            self._last_choice = panel_name

# ex:et:ts=4:
