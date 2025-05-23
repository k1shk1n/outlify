from typing import Sequence


__all__ = ['Colors', 'Styles', 'AnsiCodes']


CSI = '\033['  # Control Sequence Introducer
SGR = 'm'      # Select Graphic Rendition suffix


def code_to_ansi(*codes: int) -> str:
    return f"{CSI}{';'.join(map(str, codes))}{SGR}"


class AnsiCodes:
    def __init__(self):
        for name in (name for name in dir(self) if not name.startswith('_')):
            value = getattr(self, name)
            if isinstance(value, Sequence):
                setattr(self, name, code_to_ansi(*value))
            else:
                setattr(self, name, code_to_ansi(value))


class AnsiColorsCodes(AnsiCodes):
    # standard colors
    black   = 30
    red     = 31
    green   = 32
    yellow  = 33
    blue    = 34
    magenta = 35
    cyan    = 36
    white   = 37

    # bright colors
    gray    = 90
    crimson = 91
    lime    = 92
    gold    = 93
    skyblue = 94
    violet  = 95
    aqua    = 96
    snow    = 97

    default = 39
    # reset all styles include colors/styles
    reset   = 0


class AnsiBackColorsCodes(AnsiCodes):
    # standard colors
    black   = 40
    red     = 41
    green   = 42
    yellow  = 43
    blue    = 44
    magenta = 45
    cyan    = 46
    white   = 47

    # bright colors
    gray    = 100
    crimson = 101
    lime    = 102
    gold    = 103
    skyblue = 104
    violet  = 105
    aqua    = 106
    snow    = 107

    default = 49
    # reset all styles include colors/styles
    reset   = 0


class AnsiStylesCodes(AnsiCodes):
    bold              = 1
    dim               = 2
    italic            = 3
    underline         = 4
    blink             = 5
    inverse           = 7
    hidden            = 8
    crossed_out       = 9

    reset_bold        = 22
    reset_dim         = 22
    reset_italic      = 23
    reset_underline   = 24
    reset_blink       = 25
    reset_inverse     = 27
    reset_hidden      = 28
    reset_crossed_out = 29

    default           = 22
    # reset all styles include colors/styles
    reset             = 0


Colors = AnsiColorsCodes()
Back = AnsiBackColorsCodes()
Styles = AnsiStylesCodes()

class CustomAnsiColorsCodes(AnsiCodes):
    branded = [38, 2, 255, 165, 0]

custom = CustomAnsiColorsCodes()
print(f'{custom.branded}123')