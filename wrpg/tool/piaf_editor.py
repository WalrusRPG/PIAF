import json
import gi
from ..piaf import common
from ..piaf import pack
from ..piaf.common import FileType
from ..piaf.common import CompressionType
from os import path
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PIAFMainWindow:

        def clear_tree_view(self):
            self.tree_view.get_model().clear()

        def update_tree_view(self):
                index = 0
                tv_len = len(self.tree_view.get_model())
                for f in self.files:
                        if index >= tv_len:
                                self.tree_view.get_model().append([f["name"], f["path"], self.type_model[f["type"]][1], self.compression_model[f["compression"]][1]])
                        else:
                                self.tree_view.get_model()[index][0] = f["name"]
                                self.tree_view.get_model()[index][1] = f["path"]
                                self.tree_view.get_model()[index][2] = self.type_model[f["type"]][1]
                                self.tree_view.get_model()[index][3] = self.compression_model[f["compression"]][1]
                        index += 1

        def clear_entry_view(self):
                self.file_name_entry.set_text("")
                self.file_path_entry.set_text("")
                self.file_type_entry.set_active(0)
                self.file_compression_entry.set_active(0)


        def select_entry(self, entry):
                model, tree_iter = entry.get_selection().get_selected()
                if tree_iter == None:
                        return
                self.selected_entry = model.get_path(tree_iter).get_indices()[0]
                f = self.files[self.selected_entry]
                self.file_name_entry.set_text(f['name'])
                self.file_path_entry.set_text(f['path'])
                self.file_type_entry.set_active(f['type'])
                self.file_compression_entry.set_active(f['compression'])

        def new_archive(self, button):
                self.files = []
                self.selected_entry = None
                self.clear_tree_view()
                self.update_tree_view()
                self.clear_entry_view()

        def open_archive(self, button):
            file_chooser = Gtk.FileChooserDialog("Open", self.window, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            json_filter = Gtk.FileFilter()
            json_filter.set_name('JSON file')
            json_filter.add_pattern('*.json')
            file_chooser.add_filter(json_filter)
            response = file_chooser.run()           
            if response == Gtk.ResponseType.OK:
                with open(file_chooser.get_filename(), 'r') as f:
                        j = json.load(f)
                        if j["version"] == common.PIAF_VERSION:
                            self.files = []
                            for element in j["file_entries"]:
                                f = {}
                                f["path"] = element["path"]
                                f["name"] = element["file_name"]
                                f["type"] = element["file_type"]
                                f["compression"] = element["compression_type"]
                                self.files.append(f)
                file_chooser.destroy()
                self.update_tree_view()

        def save_archive(self, button):
            file_chooser = Gtk.FileChooserDialog("Save", self.window, Gtk.FileChooserAction.SAVE,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            json_filter = Gtk.FileFilter()
            json_filter.set_name('JSON file')
            json_filter.add_pattern('*.json')
            file_chooser.add_filter(json_filter)
            response = file_chooser.run()           
            if response == Gtk.ResponseType.OK:
                j = {"version": common.PIAF_VERSION, "file_entries": [{"path": f["path"], "file_name":f["name"], "compression_type":f["compression"], "file_type":f["type"]} for f in self.files]}
                string = json.dumps(j)
                with open(file_chooser.get_filename(), 'w+') as f:
                    f.write(string)
            file_chooser.destroy()

        def compile_file(self, button):
            file_chooser = Gtk.FileChooserDialog("Save", self.window, Gtk.FileChooserAction.SAVE,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            wrf = Gtk.FileFilter()
            wrf.set_name('WalrusRPG Archive file')
            wrf.add_pattern('*.wrf')
            file_chooser.add_filter(wrf)
            response = file_chooser.run()           
            if response == Gtk.ResponseType.OK:
                j = {"version": common.PIAF_VERSION, "file_entries": [{"path": f["path"], "file_name":f["name"].encode('ascii'), "compression_type":CompressionType(f["compression"]), "file_type":FileType(f["type"]), "data":open(f["path"], "rb").read()} for f in self.files]}
                arc = pack.pack_archive(j)
                with open(file_chooser.get_filename(), 'wb+') as f:
                    f.write(arc)
            file_chooser.destroy()
           

        def add_file(self, button):
            file_chooser = Gtk.FileChooserDialog("Open", self.window, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            response = file_chooser.run()
            if response == Gtk.ResponseType.OK:
                    selected_path = file_chooser.get_filename()
                    self.files.append({"name": path.basename(selected_path)[0:8], "path": selected_path, "type":0})
            file_chooser.destroy()
            self.update_tree_view()

        def delete_file(self, button):
            if self.selected_entry == None:
                    return
            self.files.pop(self.selected_entry)
            self.tree_view.get_model().remove(self.tree_view.get_model().iter_nth_child(None, self.selected_entry))
            print(self.selected_entry)
            if self.selected_entry == 0 and len(self.tree_view.get_model()) == 0:
                    self.selected_entry = None
                    self.clear_entry_view()

        def update_entry(self, edited_field):
            if self.selected_entry == None:
                    return
            if edited_field is self.file_name_entry:
                    self.files[self.selected_entry]["name"] = self.file_name_entry.get_text()
            elif edited_field is self.file_path_entry:
                    self.files[self.selected_entry]["path"] = self.file_path_entry.get_text()
            elif edited_field is self.file_type_entry:
                    self.files[self.selected_entry]["type"] = self.file_type_entry.get_model()[self.file_type_entry.get_active_iter()][0]
            elif edited_field is self.file_compression_entry:
                    self.files[self.selected_entry]["compression"] = self.file_compression_entry.get_model()[self.file_compression_entry.get_active_iter()][0]

            self.update_tree_view()

        def check_if_file_exists(self, field):
            if not field.get_text():
                    field.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, None)
                    field.set_icon_tooltip_text(Gtk.EntryIconPosition.PRIMARY, None)
            elif not path.exists(field.get_text()):
                    field.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, "gtk-dialog-error")
                    field.set_icon_tooltip_text(Gtk.EntryIconPosition.PRIMARY, "File doesn't exist.")
            elif not path.isfile(field.get_text()):
                    field.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, "gtk-dialog-error")
                    field.set_icon_tooltip_text(Gtk.EntryIconPosition.PRIMARY, "This is not a file.")
            else:
                    field.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, None)
                    field.set_icon_tooltip_text(Gtk.EntryIconPosition.PRIMARY, None)

        def __init__(self):
            builder = Gtk.Builder()
            builder.add_from_file(path.join(path.dirname(__file__),"piaf_editor.glade"))
            builder.connect_signals(self)

            self.file_model = builder.get_object("files_view_model")
            self.type_model = builder.get_object("file_type_model")
            for t in FileType:
                self.type_model.append([t.value, t.name])
            self.compression_model = builder.get_object("file_compression_model")
            for c in CompressionType:
                self.compression_model.append([c.value, c.name])
            self.tree_view = builder.get_object("list_view")
            self.selected_entry = builder.get_object("selected_entry")

            self.file_name_entry = builder.get_object("file_name")
            self.file_path_entry = builder.get_object("file_path")
            self.file_type_entry = builder.get_object("file_type")
            self.file_compression_entry = builder.get_object("file_compression")
            self.file_path = builder.get_object("file_path")

            column = Gtk.TreeViewColumn('Internal name', Gtk.CellRendererText(), text=0)
            column.set_clickable(True)
            column.set_resizable(True)
            self.tree_view.append_column(column)

            column = Gtk.TreeViewColumn('Path', Gtk.CellRendererText(), text=1)
            column.set_clickable(True)
            column.set_resizable(True)
            self.tree_view.append_column(column)

            column = Gtk.TreeViewColumn('Type', Gtk.CellRendererText(), text=2)
            column.set_clickable(True)
            column.set_resizable(True)
            self.tree_view.append_column(column)

            column = Gtk.TreeViewColumn('Compression', Gtk.CellRendererText(), text=3)
            column.set_clickable(True)
            column.set_resizable(True)
            self.tree_view.append_column(column)

            self.new_archive(None)


            self.window = builder.get_object("main")

