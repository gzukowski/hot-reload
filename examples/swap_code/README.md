## How to run

From `examples/swap_code`:

```
uv run python try_swap.py
```

1. The script prints the state before reload and waits on `input(...)`.
2. Edit `mod.py` and change the returned string (e.g. `"v1"` → `"v2"`), then save.
3. Press Enter: the script reloads `mod`, prints the state, then swaps the code
   into the old function and prints the state again.

## Example output

```
--- before reload ---
mod.hello() = 'v1'    hello() = 'v1'
mod.hello        @ 0x20040044540   code @ 0x2004005aa70
hello (from mod) @ 0x20040044540   code @ 0x2004005aa70
mod.hello is hello: True

--- after reload (before swap) ---
mod.hello() = 'v2'    hello() = 'v1'
mod.hello        @ 0x20040044680   code @ 0x2003fcaa320      <- new function, new code
hello (from mod) @ 0x20040044540   code @ 0x2004005aa70      <- old function, old code
mod.hello is hello: False

--- after swap ---
mod.hello() = 'v2'    hello() = 'v2'
mod.hello        @ 0x20040044540   code @ 0x2003fcaa320      <- old function, NEW code
hello (from mod) @ 0x20040044540   code @ 0x2003fcaa320      <- same object
mod.hello is hello: True
```

The middle block is the same problem as in `new_object`. The last block is the fix:
the function address is back to the original `...4540`, but its code address is
now the new `...a320`.

## Function object vs code object

A function in Python is two objects:

- the **code object** (`hello.__code__`): the compiled bytecode, constants
  (like `"v1"`), local variable names. This is "what the function does".
- the **function object** (`hello`): a wrapper around the code that also holds
  its globals (`__globals__`), default arguments (`__defaults__`), closure
  (`__closure__`), name, docstring. This is what every reference points to.

`__code__` is a writable attribute, so we can keep the function object and
replace only the code inside:

```python
old = mod.hello        # save the old function before reload rebinds the name
importlib.reload(mod)  # creates a new function object
new = mod.hello

old.__code__ = new.__code__  # new code into the OLD object
mod.hello = old              # module name points to the old object again
```

After this every reference (`mod.hello`, `from mod import hello`, a GUI callback,
anything) points to one object, and that object runs the new code:

```
mod.__dict__["hello"] ──┐
                        ├──► function @ ...4540  ──►  code: return "v2"
try_reload.hello  ──────┘

                             function @ ...4680  (new one, no longer referenced, garbage collected)
```
