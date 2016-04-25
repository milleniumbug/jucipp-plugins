import jucipp, os, gi, traceback, functools, uuid
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from os import path

def add_menu(position, label, items) :
    plugin_menu = jucipp.get_gio_plugin_menu()
    sub_menu = Gio.Menu.new()
    i = 0
    app = Gio.Application.get_default()
    for item in items :
      sub_menu.insert(i, item['label'], 'app.'+item['action'])
      i = i + 1
      python_action = Gio.SimpleAction.new(item['action'], None)
      python_action.connect('activate', item['method'])
      app.add_action(python_action)
    if plugin_menu.get_n_items() >= position :
      plugin_menu.remove(position)
    plugin_menu.insert_submenu(position, label, sub_menu)
    
def add_commands(command_list):
  def item_from_cmd(cmd):
    return {
      'label': cmd[0],
      'action': str(uuid.uuid4()).replace("-","").upper(),
      'method': lambda action, param: jucipp.directories.open(cmd[1])
    }
  
  items = list(map(item_from_cmd, command_list))
  add_menu(3, '_Project jumpboard', items)
  
def run_command(cmd):
  app = Gio.Application.get_default()
  app.run_command(cmd)
    
def init() :
  cmds = [
    ("juCi", "/home/milleniumbug/dokumenty/PROJEKTY/NotMine/jucipp"),
    ("gdbplz", "/home/milleniumbug/dokumenty/PROJEKTY/InDevelopment/gdbplz"),
  ]
  add_commands(cmds)

init()
