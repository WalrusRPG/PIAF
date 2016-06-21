#!/usr/bin/env python3
from wrpg.tool.piaf_editor import PIAFMainWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
if __name__ == '__main__':

    w = PIAFMainWindow()
    w.window.connect("destroy", Gtk.main_quit)
    w.window.show()
    Gtk.main()
