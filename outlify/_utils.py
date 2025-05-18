from typing import Optional, Union, Any
import shutil

from outlify.style import Align, Style
from outlify._ansi import AnsiStylesCodes


EMPTY = Style()
RESET = Style(AnsiStylesCodes.reset)


def resolve_width(width: Optional[int]) -> int:
    if isinstance(width, int):
        return width
    if width is not None:
        raise ValueError(f'Invalid type for width: {width} is not int')

    try:
        return shutil.get_terminal_size().columns
    except (AttributeError, OSError):
        return 80  # Fallback width


def parse_title_align(align: Union[str, Align]) -> Align:
    return _parse_class(align, Align)


def parse_style(style: Union[str, Style]) -> Style:
    return _parse_class(style, Style)


def _parse_class(element: Union[str, Any], cls: Any) -> Any:
    if isinstance(element, cls):
        return element
    return cls(element)


def get_reset_by_style(style: Style) -> Style:
    """ Return the appropriate reset code for the given style

    If the style is empty, returns an empty reset.
    Otherwise, returns the standard reset
    """
    return RESET if style != '' else EMPTY
