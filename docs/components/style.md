# Styles

The **Style** module allows you to style **Outlify** elements

## `Style`
The main class that is used to work with styles.

the class itself is inherited from `str`, as the result of its work will be a string of ansi escape sequences.

It accepts any number of elements of types:

1. `int`: ansi codes
2. `AnsiColorsCodes` / `AnsiStylesCodes` / base enum `AnsiCodes`: built-in codes
3. `str`: string separated by spaces, where the codes match the name of the codes in `AnsiColorsCodes` / `AnsiStylesCodes`,
e.g. `red bold`

## `AnsiColorsCodes`
`enum` which contains codes for styling text by color

### Available values

| Value     | Code | Comments                               |
|-----------|:----:|----------------------------------------|
| `black`   | `30` |
| `red`     | `31` |
| `green`   | `32` |
| `yellow`  | `33` |
| `blue`    | `34` |
| `magenta` | `35` |
| `cyan`    | `36` |
| `white`   | `37` |
| `default` | `39` |
| `gray`    | `90` |
| `reset`   | `0`  | reset all styles include colors/styles |

!!! tip

    You can check available using `AnsiColorsCodes.get_available_values()`

## `AnsiStylesCodes`
`enum` which contains codes for styling text by highlighting

### Available values:

| Value         | Code | Comments                               |
|---------------|:----:|----------------------------------------|
| `bold`        | `1`  |
| `dim`         | `2`  |
| `italic`      | `3`  |
| `underline`   | `4`  |
| `crossed_out` | `9`  |
| `default`     | `35` |
| `reset`       | `0`  | reset all styles include colors/styles |

!!! tip

    You can check available using `AnsiStylesCodes.get_available_values()`

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