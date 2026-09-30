import importlib

import mod
from mod import hello  # copies the reference; not linked to mod.hello afterwards


def show(label):
    # hex(id(obj)) is the object's memory address in CPython
    print(f"--- {label} ---")
    print(f"mod.hello() = {mod.hello()!r:6}  hello() = {hello()!r}")
    print(f"module mod       @ {hex(id(mod))}")
    print(f"mod.hello        @ {hex(id(mod.hello))}   code @ {hex(id(mod.hello.__code__))}")
    print(f"hello (from mod) @ {hex(id(hello))}   code @ {hex(id(hello.__code__))}")
    print(f"mod.hello is hello: {mod.hello is hello}")
    print()


show("before reload")

input("change mod.py, save, then press enter to continue...")
importlib.reload(mod)  # re-executes mod.py in the same module object -> `def` creates a new function

show("after reload")
