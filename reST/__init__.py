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

from gi.repository import GObject, Gedit

from .restructuredtext import RestructuredtextHtmlPanel


class ReStructuredTextPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ReStructuredTextPlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

        self._panel = None

    def do_activate(self):
        panel_name = 'GeditReStructuredTextPanel'
        panel_title = 'reStructuredText Preview'

        self._panel = RestructuredtextHtmlPanel()
        self._panel.update_view(self.window)
        self._panel.show()

        bottom = self.window.get_bottom_panel()
        try:
            bottom.add_titled(self._panel, panel_name, panel_title)
        except AttributeError as err:
            print('Falling back to old implementation. Reason: %s' % err)
            bottom.add_item(self._panel, panel_name, panel_title)

    def do_deactivate(self):
        self._panel.clear_view()
        bottom = self.window.get_bottom_panel()
        bottom.remove(self._panel)

    def do_update_state(self):
        self._panel.update_view(self.window)

# ex:et:ts=4:
