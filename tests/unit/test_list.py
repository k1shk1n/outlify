from typing import Sequence, Optional, Any

import pytest

from outlify.list import ListBase, TitledList
from outlify.style import Style

from .common import EMPTY, RESET


class ReleasedListBase(ListBase):
    def __init__(
            self, content: Sequence[Any], *, width: Optional[int] = None, title: str = 'Content',
            separator: str = '  '
    ):
        self.separator = separator
        super().__init__(content, width=width, title=title, title_separator=': ')

    def get_content(self, content: list[str], *, width: int) -> str:
        return ''


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,count,style,reset,result',
    [
        ('TITLE', 0, EMPTY, EMPTY, 'TITLE (0)'),
        ('fake', 10, EMPTY, EMPTY, 'fake (10)'),
        ('minus', -10, EMPTY, EMPTY, 'minus (-10)'),
        ('TITLE', 0, Style('bold'), RESET, '\033[1mTITLE (0)\033[0m'),
    ]
)
def test_get_title(title: str, count: int, style: Style, reset: Style, result: str):
    assert ReleasedListBase([])._get_title(title, count=count, style=style, reset=reset) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'content,result',
    [
        ([], []),
        ([123, 321], ['123', '321']),
        (['test'], ['test']),
        (
            [1, 'test', (1, 'test'), [1, 'test'], {'test': 1}],
            ['1', 'test', '(1, \'test\')', '[1, \'test\']', '{\'test\': 1}']
        ),
    ]
)
def test_prepared_content(content: Sequence[Any], result: list[str]):
    assert ReleasedListBase([])._prepare_content(content) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'content,title,separator,result',
    [
        ([], None, None, 'Content (0)'),
        ([1, 2, 3], None, None, 'Content (3): 1  2  3'),
        ([1, '2', {1: '2'}], None, None, 'Content (3): 1  2  {1: \'2\'}'),
        (['first', 'second'], 'Words', None, 'Words (2): first  second'),
        (['first', 'second'], None, ', ', 'Content (2): first, second'),
        (['ruff@1.0.0', 'pytest@1.2.3'], 'Packages', ' :: ', 'Packages (2): ruff@1.0.0 :: pytest@1.2.3'),
    ]
)
def test_titled_list(content: Sequence[Any], title: str | None, separator: str | None, result: str):
    params = {}
    if title is not None:
        params['title'] = title
    if separator is not None:
        params['separator'] = separator
    assert str(TitledList(content, **params)) == result
