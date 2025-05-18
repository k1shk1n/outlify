from typing import Optional, Union

import pytest

from outlify._ansi import Style, AnsiCodes, AnsiColorsCodes, AnsiStylesCodes


@pytest.mark.unit
@pytest.mark.parametrize(
    'codes,result',
    [
        ((), ''),
        ((None,), ''),
        ((1,), '\033[1m'),
        ((1,2), '\033[1;2m'),

        (('bold',), '\033[1m'),
        (('bold dim',), '\033[1;2m'),
        (('bold', 'dim'), '\033[1;2m'),

        ((AnsiColorsCodes.black,), '\033[30m'),
        ((AnsiColorsCodes.black, AnsiColorsCodes.red), '\033[30;31m'),
        ((AnsiStylesCodes.bold,), '\033[1m'),
        ((AnsiStylesCodes.bold, AnsiStylesCodes.dim), '\033[1;2m'),

        ((AnsiColorsCodes.black, AnsiStylesCodes.bold), '\033[30;1m'),
        ((AnsiStylesCodes.bold, AnsiColorsCodes.black), '\033[1;30m'),
    ]
)
def test_style(codes: tuple[Optional[Union[int, str, AnsiCodes]]], result: str):
    assert Style(*codes) == result
