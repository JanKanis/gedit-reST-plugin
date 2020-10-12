# -*- coding: utf-8 -*-

# restructuredtext.py - reStructuredText HTML preview panel
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

gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')

from docutils.core import publish_parts
from gi.repository import Gtk, WebKit2, GLib
from os.path import abspath, dirname, join
import threading


class RestructuredtextHtmlPanel(Gtk.ScrolledWindow):
    """
    A Gtk panel displaying HTML rendered from ``.rst`` source code.
    """
    MIME_TYPE = 'text/html'
    ENCODING = 'UTF-8'
    TEMPLATE = u"""<!DOCTYPE html>
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

        self.lock = threading.Lock()
        self.alive = True
        self.event = threading.Event()
        self.worker = threading.Thread(target=self.rest_parser_thread, name="gedit-reST-plugin worker")
        self.worker.start()
        self.show_reST = False

        module_dir = dirname(abspath(__file__))
        css_file = join(module_dir, styles_filename)
        with open(css_file, 'r') as styles:
            self.styles = styles.read()

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.view = WebKit2.WebView()
        self.add(self.view)
        self.view.show()

    def update_view(self, parent_window):
        view = parent_window.get_active_view()
        language = None
        if view:
            source_language = \
                parent_window.get_active_document().get_language()
            if source_language:
                language = source_language.get_name()

        if language == 'reStructuredText':
            doc = view.get_buffer()
            start = doc.get_start_iter()
            end = doc.get_end_iter()

            if doc.get_selection_bounds():
                start = doc.get_iter_at_mark(doc.get_insert())
                end = doc.get_iter_at_mark(doc.get_selection_bound())

            text = doc.get_text(start, end, False)

            self.show_rest = True
            with self.lock:
                self.parent_window = parent_window
                self.text = text
            # Only start the background thread once there is idle time, otherwise it can hold the GIL for too long, blocking the editor.
            GLib.idle_add(self.set_event)
        else:
            self.show_rest = False
            html = '<h3>reStructuredText Preview</h3>\n' \
                   '<p>' \
                   '<em>Switch file language to</em> reStructuredText ' \
                   '<em>to render the document</em>' \
                   '</p>'
            base_uri = ''

            self.view.load_html(self.TEMPLATE.format(
                body=html, css=self.styles
            ), base_uri)

    def set_event(self):
        self.event.set()
        return False

    def update_callback(self, html, parent_window):
        if not self.show_rest:
            return False

        location = parent_window.get_active_document().get_location()
        base_uri = location.get_uri() if location else ''

        self.view.load_html(self.TEMPLATE.format(
            body=html, css=self.styles
        ), base_uri)

        return False  # stop idle_add from calling us again

    def clear_view(self):
        self.alive = False
        self.show_rest = False
        self.event.set()
        self.view.load_html('', '')

    def rest_parser_thread(self):
        while True:
            self.event.wait()  # Block until there's something to do
            self.event.clear()

            if self.alive == False:
                return

            with self.lock:
                parent_window, text = self.parent_window, self.text
                self.parent_window, self.text = None, None
            if not text:
                continue

            html = publish_parts(text, writer_name='html')['html_body']
            # We're not allowed to call Gtk methods on this thread
            GLib.idle_add(self.update_callback, html, parent_window)

