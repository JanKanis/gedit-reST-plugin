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

import os
import sys
import threading

from docutils.core import publish_parts
from enum import Enum
from os.path import abspath, dirname, join

from gi.repository import GLib, Gtk, WebKit2

class State(Enum):
    NON_REST = 1
    REST = 2
    SELECTION = 3
    EXIT = 4

DEBUG = False
def debug(*args):
    if DEBUG:
        print(*args, file=sys.stderr)


class PreviewArgs:
    def __init__(self, text=None, html=None, html_type=None):
        self.text, self.html, self.html_type = text, html, html_type


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
    {scripts}
    </body>
    </html>
    """

    def __init__(self, parent_window, panel, styles_filename='restructuredtext.css'):
        Gtk.ScrolledWindow.__init__(self)

        self.parent_window = parent_window
        self.panel = panel

        self.lock = threading.Lock()
        self.event = threading.Event()

        # state is the state we want to be in (and in which the text area is). It is updated when the text
        # area updates.
        self.state = State.NON_REST

        # To restore scroll positions after redrawing the preview, and across selecting text. Contains the most recent
        # position when we were showing a (non-selection) reST preview.
        self.last_position = None
        # scroll_position_valid indicates if the preview panel currently contains a reST (non-selection) preview
        self.scroll_position_valid = False

        module_dir = dirname(abspath(__file__))
        css_file = join(module_dir, styles_filename)
        with open(css_file, 'r') as styles:
            self.styles = styles.read()

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.viewinit = False

    def show_view(self):
        if not self.viewinit:
            self.view = WebKit2.WebView()
            self.add(self.view)
            self.worker = threading.Thread(target=self.rest_parser_thread, name="gedit-reST-plugin worker")
            self.worker.start()

            self.viewinit = True
            debug("view started")
        self.view.show()

    def hide_view(self):
        if self.viewinit:
            self.view.hide()

    def is_visible(self):
        return self.panel.get_visible_child() == self

    def update_view(self):
        if self.state == State.EXIT:
            debug("EXIT")
            return

        if self.is_visible():
            self.show_view()
        else:
            debug("NOT VISIBLE")
            self.hide_view()
            return

        view = self.parent_window.get_active_view()
        language = None
        if view:
            source_language = self.parent_window.get_active_document().get_language()
            if source_language:
                language = source_language.get_name()

        if language == 'reStructuredText':
            doc = view.get_buffer()
            if doc.get_selection_bounds():
                self.state = State.SELECTION
                debug("state = SELECTION")
                start = doc.get_iter_at_mark(doc.get_insert())
                end = doc.get_iter_at_mark(doc.get_selection_bound())
            else:
                self.state = State.REST
                debug("state = REST")
                start = doc.get_start_iter()
                end = doc.get_end_iter()

            text = doc.get_text(start, end, False)

            with self.lock:
                self.preview_args = PreviewArgs(text=text, html_type=self.state)
            # Only start the background thread once there is idle time, otherwise it can hold the GIL for too long,
            # blocking the editor.
            GLib.idle_add(self.set_event)
        else:
            self.state = State.NON_REST
            debug("state = NON_REST")
            html = '<h3>reStructuredText Preview</h3>\n' \
                   '<p>' \
                   '<em>Switch file language to</em> reStructuredText ' \
                   '<em>to render the document</em>' \
                   '</p>'

            self.save_scroll_position(PreviewArgs(html=html, html_type=State.NON_REST))

    def set_event(self):
        self.event.set()
        return False

    def save_scroll_position(self, args):
        if self.state == State.EXIT:
            return False

        if self.scroll_position_valid:
            debug("saving scroll position")
            self.view.run_javascript("[window.scrollX, window.scrollY]",
                            None, self.display_html, args)
        else:
            self.display_html(None, None, args)
        return False  # stop idle_add from calling us again

    def display_html(self, _view, scrollresult, args):
        if self.state == State.EXIT:
            return

        if scrollresult:
            try:
                self.last_position = self.view.run_javascript_finish(scrollresult) \
                                        .get_js_value().to_string()
                debug("last_position = ", self.last_position)
            except GLib.Error as e:
                print("Error retrieving reST preview scroll position:", e,
                      file=sys.stderr)

        if args.html_type != self.state:
            debug("stale callback", self.state, ", not rendering html")
            return

        base_uri = ''
        if self.state in [State.REST, State.SELECTION]:
            location = self.parent_window.get_active_document().get_location()
            base_uri = location.get_uri() if location else ''

        script = ''
        debug("last_position:", self.last_position)
        if self.state == State.REST and self.last_position:
            script = f"<script>window.scroll({self.last_position})</script>\n"
            debug("restoring position in new html")
        document = self.TEMPLATE.format(body=args.html, css=self.styles, scripts=script)

        debug("Rendering", self.state, "html")
        self.view.load_html(document, base_uri)
        self.scroll_position_valid = (self.state == State.REST)
        debug("scroll_position_valid =", self.scroll_position_valid)

    def clear_view(self):
        self.state = State.EXIT
        debug("state = EXIT")
        self.parent_window, self.panel = None, None
        self.event.set()
        if self.viewinit:
            self.view.load_html('', '')

    def rest_parser_thread(self):
        try:
            tid = int(os.readlink('/proc/thread-self').split('/')[-1])
            debug("reST preview rendering thread id", tid)
            # Set nice +10 and SCHED_BATCH on this thread
            exit_code = os.system(f'schedtool -n 10 -B {tid}')
            if exit_code != 0:
                raise OSError()
        except OSError as e:
            debug("Unable to set batch priority for reST preview rendering thread. "
                  "This is only supposed to work on Linux")

        while True:
            self.event.wait()  # Block until there's something to do
            self.event.clear()

            if self.state == State.EXIT:
                return

            with self.lock:
                args = self.preview_args
                self.preview_args = None
            if not args:
                continue

            args.html = publish_parts(args.text, writer_name='html')['html_body']
            args.text = None
            # We're not allowed to call Gtk methods on this thread
            GLib.idle_add(self.save_scroll_position, args)
