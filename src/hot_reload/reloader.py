"""Reload a module in place: existing function objects get the new code."""

import importlib
import types


def reload_module(module: types.ModuleType) -> None:
    old_functions = {
        name: obj for name, obj in vars(module).items() if isinstance(obj, types.FunctionType)
    }

    importlib.reload(module)

    for name, old in old_functions.items():
        new = getattr(module, name, None)
        if new is old:
            print(f"[hot-reload] {module.__name__}.{name}: unchanged")
            continue  # not defined in this file, e.g. `from os.path import join` or removed function
        try:
            _patch_function(old, new)
        except ValueError as exc:
            # Different number of closure variables; keep the new function under the name.
            print(f"[hot-reload] {module.__name__}.{name}: cannot patch in place: {exc}")
            continue
        setattr(module, name, old)


def _patch_function(old: types.FunctionType, new: types.FunctionType) -> None:
    old.__code__ = new.__code__  # must be first: raises ValueError before anything is changed
    old.__defaults__ = new.__defaults__
    old.__kwdefaults__ = new.__kwdefaults__
    old.__doc__ = new.__doc__
