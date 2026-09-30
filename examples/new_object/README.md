## How to run

From `examples/new_object`:

```
uv run python try_reload.py
```

1. The script prints the state before reload and waits on `input(...)`.
2. Edit `mod.py` and change the returned string (e.g. `"v1"` → `"v2"`), then save.
3. Press Enter: the script calls `importlib.reload(mod)` and prints the state after reload.

## Example output

Your addresses will differ. What matters is which ones change and which don't:

```
--- before reload ---
mod.hello() = 'v1'    hello() = 'v1'
module mod       @ 0x19786efe570
mod.hello        @ 0x1978700b880   code @ 0x19786e79620
hello (from mod) @ 0x1978700b880   code @ 0x19786e79620
mod.hello is hello: True

--- after reload ---
mod.hello() = 'v2'    hello() = 'v1'
module mod       @ 0x19786efe570                              <- same module
mod.hello        @ 0x19787020180   code @ 0x1978702a730       <- NEW function, new code
hello (from mod) @ 0x1978700b880   code @ 0x19786e79620       <- old function, old code
mod.hello is hello: False
```

In CPython, `hex(id(obj))` is the object's memory address. Two names with the
same address point to **the same** object.

## What happens

In Python a variable is just a name pointing to an object. At the start
there are two names and one function object:

```
mod.__dict__["hello"] ──┐
                        ├──► function @ ...b880  ──►  code: return "v1"
try_reload.hello  ──────┘
```

`from mod import hello` does **not** create any link to `mod.hello`. It only
copies the reference: from now on `try_reload.hello` is a separate name that
happens to point to the same object.

`importlib.reload(mod)` executes `mod.py` again, inside the same module
object (that's why the module address doesn't change). Running `def hello():`
again creates a new function object and binds it to the name `mod.hello`.
Nobody modifies the old object:

```
mod.__dict__["hello"] ─────────► function @ ...0180  ──►  code: return "v2"   (new)

try_reload.hello  ─────────────► function @ ...b880  ──►  code: return "v1"   (old, still alive)
```

The old object doesn't go away, because `try_reload.hello` still holds it.
