from functools import lru_cache
from enum import Enum
from typing import Union


__all__ = ['RESET', 'AnsiColorsCodes', 'AnsiStylesCodes', 'Style', 'wrap']


CSI = '\033['           # Control Sequence Introducer
SGR = 'm'               # Select Graphic Rendition suffix
RESET = f'{CSI}0{SGR}'


@lru_cache(maxsize=128)
def code_to_ansi(*codes: int) -> str:
    return f"{CSI}{';'.join(str(code) for code in codes)}{SGR}"


class AnsiCodes(Enum):
    @classmethod
    def get_available_values(cls) -> tuple[str, ...]:
        return tuple(value for value in dir(cls) if not value.startswith('_'))


class AnsiColorsCodes(AnsiCodes):
    black   = 30
    red     = 31
    green   = 32
    yellow  = 33
    blue    = 34
    magenta = 35
    cyan    = 36
    white   = 37
    default = 39
    gray    = 90


class AnsiStylesCodes(AnsiCodes):
    bold        = 1
    dim         = 2
    italic      = 3
    underline   = 4
    crossed_out = 9
    default     = 22


AVAILABLE_VALUES = AnsiColorsCodes.get_available_values() + AnsiStylesCodes.get_available_values()


class Style(str):
    def __new__(cls, *style_codes: Union[int, str, AnsiCodes]):
        codes = []
        for code in style_codes:
            if isinstance(code, AnsiCodes):
                codes.append(code.value)
            elif isinstance(code, str):
                codes.extend(Style._process_str(code))
            else:
                Style._validate(code)
                codes.append(code)
        return super().__new__(cls, code_to_ansi(*codes))

    @staticmethod
    def _process_str(string: str) -> list[int]:
        codes = []
        for style in string.split(' '):
            defaults = {
                'default': ValueError,
                'default_color': AnsiColorsCodes.default.value,
                'default_style': AnsiStylesCodes.default.value
            }
            if style in defaults.keys():
                codes.append(Style._process_default(style, defaults=defaults))
                continue
            color_code, style_code = getattr(AnsiColorsCodes, style, None), getattr(AnsiStylesCodes, style, None)
            if color_code is None and style_code is None:
                raise ValueError(f"Invalid style value='{style}'. Available values: {', '.join(AVAILABLE_VALUES)}")
            code = color_code or style_code
            codes.append(code.value)
        return codes

    @staticmethod
    def _process_default(style: str, *, defaults: dict[str, int]) -> int:
        default = 'default'
        value = defaults[style]
        if value is ValueError:
            raise ValueError(
                f"It was not possible to parse the '{default}' style because it is used "
                f"in {AnsiColorsCodes.__name__} and in {AnsiStylesCodes.__name__}. "
                f"If you want to use default for color use 'default_color', "
                f"if default for style - use 'default_style'"
            )
        return defaults[style]

    @staticmethod
    def _validate(code: int):
        if code not in AVAILABLE_VALUES:
            return ValueError(f'Invalid {code} code for style (for ansi codes)')


def wrap(text: str, style: Style) -> str:
    return f"{style}{text}{RESET}"


# # ТЕСТЫ ПО ПЕРФОРМАНСУ
# from datetime import datetime
#
# now1 = datetime.now()
# print('\033[31m\033[1mtext\033[0m')
# end1 = datetime.now()
#
# now2 = datetime.now()
# print('\033[31;1mtext\033[0m')
# end2 = datetime.now()
#
# print(f'раздельно: {end1 - now1}')
# print(f'вместе: {end2 - now2}')
