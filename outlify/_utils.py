from typing import Optional
import shutil


__all__ = ['resolve_width']


def resolve_width(width: Optional[int]) -> int:
    if isinstance(width, int):
        return width
    if width is not None:
        raise ValueError(f'Invalid type for width: {width} is not int')

    try:
        return shutil.get_terminal_size().columns
    except (AttributeError, OSError):
        return 80  # Fallback width
