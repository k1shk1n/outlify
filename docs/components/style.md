# Styles

## `AnsiColorsCodes`
TBD

## `AnsiStylesCodes`
TBD

## `Style`
TBD

## Advanced
### Ansi codes

!!! question

    Why ansi codes (`0`, `31`, etc) are used instead of ready-made ansi escape sequences,
    as in the same `colorama` (`\033[1m`, `\033[31m`, etc.)

Because using prepared ansi escape sequences we can get strings like `\033[1m\033[31m` 
using, for example, `f'{Style.bold}{Color.red}'`. Using ansi code we will get strings
of the form `\033[1;31m`. For a terminal, it is one operation less. And that's only if
we want to apply two styles, and if there are more styles, it's even slower.

We can compare the execution speed for these operations

```python
from time import time

def timer(text: str):
    now = time()
    print(text)
    return time() - now

timer('warp up')
x = timer('\033[31m\033[1mtext\033[0m')
y = timer('\033[31;1mtext\033[0m')

print(f'ansi escape sequences: {x:10f}')
print(f'ansi codes: {y:10f}')
print(f'{x / y:2f} times faster')
```

<div class="result" markdown>

```
warp up
text
text
----- Results -----
ansi escape sequences:   0.000005
ansi codes:   0.000004
1.166667 times faster
```

</div>

If you use a lot of styles, there may be a noticeable slowdown.