# -*- coding: utf-8 -*-

# config.py -- Config dialog
#
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
from gi.repository import Gio, Gtk

__all__ = ['RestructuredtextConfigWidget']


class RestructuredtextConfigWidget(object):

    REST_KEY_BASE = 'org.gnome.gedit.plugins.restructuredtext'
    REST_KEY_PREVIEW_PANEL = 'preview-panel'

    def __init__(self, datadir):
        object.__init__(self)

        self._ui_path = os.path.join(datadir, 'config.ui')
        # self._settings = Gio.Settings.new(self.REST_KEY_BASE)
        self._ui = Gtk.Builder()

    def configure_widget(self):
        self._ui.add_from_file(self._ui_path)

        for panel_id in ['bottom-panel', 'side-panel']:
            active = True  # self._settings.get_string(self.REST_KEY_PREVIEW_PANEL) == panel_id
            radiobutton = self._ui.get_object(panel_id)
            radiobutton.connect('toggled', self.on_button_toggled, panel_id)
            radiobutton.set_active(active)

        widget = self._ui.get_object('restructuredtext_preferences')
        return widget

    def on_button_toggled(self, radiobutton, panel_id):
        if radiobutton.get_active():
            # self._settings.set_string(self.REST_KEY_PREVIEW_PANEL, panel_id)
            print(panel_id)

# ex:et:ts=4:
