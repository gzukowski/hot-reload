## How to run

From `examples/reload_module`:

```
uv run python try_reload_module.py
```

1. The script prints the state before reload and waits on `input(...)`.
2. Edit `mod.py`, e.g. change `"v1"` → `"v2"`, change the default `greeting="hi"`
   → `greeting="hello"`, add a new function `bye()`. Save.
3. Press Enter: the script calls `reload_module(mod)` and prints the state again.

## Example output

```
--- before reload ---
hello()                = 'v1'         @ 0x1b6adbe4040
handlers['on_click']() = 'v1'         @ 0x1b6adbe4040
greet('Ann')           = 'hi Ann'     @ 0x1b6adbe40e0
functions in mod: ['hello', 'greet']

--- after reload_module ---
hello()                = 'v2'         @ 0x1b6adbe4040
handlers['on_click']() = 'v2'         @ 0x1b6adbe4040
greet('Ann')           = 'hello Ann'  @ 0x1b6adbe40e0
functions in mod: ['hello', 'greet', 'bye']
```

Every old reference (`from mod import ...`, the function stored in `handlers`)
sees the new code, and every address stays the same. The new default argument
works too, and the new function `bye` is available as `mod.bye`.

## What `reload_module` does

It's `swap_code` done for every function in the module
([src/hot_reload/reloader.py](../../src/hot_reload/reloader.py)):

1. **Snapshot.** Before reloading, collect all function objects from the
   module: `{"hello": <function @ 4040>, "greet": <function @ 40e0>}`.
   This must happen before the reload, because afterwards the module names
   already point to the new functions and the old ones are only reachable
   through other references.
2. **Reload.** `importlib.reload(module)` executes the file again. Each `def`
   creates a new function object and binds it to the module name.
3. **Patch.** For every name from the snapshot, take the new function as a
   "code donor": copy `__code__`, `__defaults__`, `__kwdefaults__`, `__doc__`
   into the old object, then point the module name back at the old object.
