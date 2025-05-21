from enum import Enum
from typing import NamedTuple

from outlify._ansi import Colors, Styles, AnsiCodes  # noqa: F401


class Align(Enum):
    left = 'left'
    center = 'center'
    right = 'right'


class BorderStyle(NamedTuple):
    lt: str
    rt: str
    lb: str
    rb: str
    headers: str
    sides: str
