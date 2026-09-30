import importlib
    
import mod
from mod import hello  # old reference held "somewhere else"


def show(label):
    # hex(id(obj)) is the object's memory address in CPython
    print(f"--- {label} ---")
    print(f"mod.hello() = {mod.hello()!r:6}  hello() = {hello()!r}")
    print(f"mod.hello        @ {hex(id(mod.hello))}   code @ {hex(id(mod.hello.__code__))}")
    print(f"hello (from mod) @ {hex(id(hello))}   code @ {hex(id(hello.__code__))}")
    print(f"mod.hello is hello: {mod.hello is hello}")
    print()


show("before reload")

input("change mod.py, save, then press enter to continue...")

old = mod.hello        # keep the old function object before reload rebinds the name
importlib.reload(mod)  # same as in new_object: `def` creates a new function object
new = mod.hello

show("after reload (before swap)")



old.__code__ = new.__code__  # put the new code into the OLD function object
mod.hello = old              # point the module name back at the old object
show("after swap")
