from typing import Sequence, Optional, Any

import pytest

from outlify.list import ListBase


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
    'title,count,result',
    [
        ('TITLE', 0, 'TITLE (0)'),
        ('fake', 10, 'fake (10)'),
        ('minus', -10, 'minus (-10)'),
    ]
)
def test_get_title(title: str, count: int, result: str):
    assert ReleasedListBase([])._get_title(title, count) == result


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
