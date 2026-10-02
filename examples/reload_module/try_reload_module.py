import mod
from mod import greet, hello  # old references held "somewhere else"

from hot_reload.reloader import reload_module

handlers = {"on_click": mod.hello}  # like a callback attached to a GUI button


def show(label):
    print(f"--- {label} ---")
    print(f"hello()                = {hello()!r:12} @ {hex(id(hello))}")
    print(f"handlers['on_click']() = {handlers['on_click']()!r:12} @ {hex(id(handlers['on_click']))}")
    print(f"greet('Ann')           = {greet('Ann')!r:12} @ {hex(id(greet))}")
    print(f"functions in mod: {[n for n in vars(mod) if not n.startswith('__')]}")
    print()


show("before reload")

input("change mod.py (return value, default greeting, add a function), save, then press enter...")
reload_module(mod)

show("after reload_module")
