# -*- coding: utf-8 -*-

# restructuredtext.py - reStructuredText HTML preview panel
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

from docutils.core import publish_parts
from gi.repository import Gtk, WebKit
from os.path import abspath, dirname, join


class RestructuredtextHtmlPanel(Gtk.ScrolledWindow):
    """
    A Gtk panel displaying HTML rendered from ``.rst`` source code.
    """
    MIME_TYPE = 'text/html'
    ENCODING = 'UTF-8'
    TEMPLATE = """<!DOCTYPE html>
    <html>
    <head>
        <style type="text/css">
            {css}
        </style>
    </head>
    <body>
    {body}
    </body>
    </html>
    """

    def __init__(self, styles_filename='restructuredtext.css'):
        Gtk.ScrolledWindow.__init__(self)

        module_dir = dirname(abspath(__file__))
        css_file = join(module_dir, styles_filename)
        with open(css_file, 'r') as styles:
            self.styles = styles.read()

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.view = WebKit.WebView()
        self.add(self.view)
        self.view.show()

    def update_view(self, parent_window):
        view = parent_window.get_active_view()
        if not view:
            html = '<p>reStructuredText Preview</p>'
            base_uri = ''
        else:
            doc = view.get_buffer()
            start = doc.get_start_iter()
            end = doc.get_end_iter()

            if doc.get_selection_bounds():
                start = doc.get_iter_at_mark(doc.get_insert())
                end = doc.get_iter_at_mark(doc.get_selection_bound())

            text = doc.get_text(start, end, False)
            html = publish_parts(text, writer_name='html')['html_body']
            base_uri = parent_window.get_active_document().get_location().get_uri()

        self.view.load_string(self.TEMPLATE.format(
            body=html, css=self.styles
        ), self.MIME_TYPE, self.ENCODING, base_uri)

    def clear_view(self):
        self.view.load_string('', self.MIME_TYPE, self.ENCODING, '')
