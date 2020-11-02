# -*- coding: utf-8 -*-
"""
config.py -- Config dialog
"""
# Copyright (C) 2020 - Peter Bittner
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
REST_KEY_BASE = 'org.gnome.gedit.plugins.restructuredtext'
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
        "return the singleton instance"
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

    def get_panel(self):
        """
        Return the name of the configured display panel of the gedit window.
        """
        panels = {
            0: 'bottom',
            1: 'side',
        }
        return panels[self.get_panel_index()]

    def get_panel_index(self):
        return self.settings.get_int(REST_KEY_PREVIEW_PANEL)

    def set_panel_index(self, index):
        self.settings.set_int(REST_KEY_PREVIEW_PANEL, index)

    def connect(self, callback, *args):
        return self.settings.connect("changed::"+REST_KEY_PREVIEW_PANEL,
                                     callback, *args)

    def disconnect_by_func(self, callback_func):
        self.settings.disconnect_by_func(callback_func)


class RestructuredtextConfigWidget:
    """
    Preferences dialog factory.
    """

    def __init__(self, parent):
        self._parent = parent
        datadir = parent.plugin_info.get_data_dir()
        self._ui_path = os.path.join(datadir, 'config.ui')
        self._ui = Gtk.Builder()
        self._settings = Settings.get()

    def configure_widget(self):
        self._ui.add_from_file(self._ui_path)

        configured_panel = self._settings.get_panel_index()

        for index, panel_id in enumerate(REST_PREVIEW_PANELS):
            radiobutton = self._ui.get_object(panel_id)
            radiobutton.connect('toggled', self.on_button_toggled, panel_id)
            radiobutton.set_active(configured_panel == index)

        widget = self._ui.get_object('restructuredtext_preferences')
        return widget

    def on_button_toggled(self, radiobutton, panel_id):
        if radiobutton.get_active():
            # self._parent.do_deactivate()
            index = REST_PREVIEW_PANELS.index(panel_id)
            self._settings.set_panel_index(index)
            # self._parent.do_activate()

# ex:et:ts=4:
