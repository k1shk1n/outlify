from typing import Union, Optional

import pytest

from outlify.panel import PanelBase, Panel, ParamsPanel
from outlify.styles import Align, BorderStyle


class ReleasedPanelBase(PanelBase):
    def __init__(
            self, content: str, *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            border_style: Union[str | BorderStyle] = '╭╮╰╯─│'
    ):
        super().__init__(
            content, width=width,
            title=title, title_align=title_align,
            subtitle=subtitle, subtitle_align=subtitle_align,
            border_style=border_style
        )

    def get_content(self, content: str, *, width: int, char: str) -> str:
        return ''


@pytest.mark.unit
@pytest.mark.parametrize(
    'align,result',
    [
        ('left', Align.left),
        ('center', Align.center),
        ('right', Align.right),
        (Align.left, Align.left),
        (Align.center, Align.center),
        (Align.right, Align.right),
    ]
)
def test_resolve_title_align(align: Union[str, Align], result: Align):
    panel = ReleasedPanelBase('test')
    assert panel._resolve_title_align(align) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'width,result',
    [
        (10, 6),     # small size
        (80, 76),    # default size
        (160, 156),  # big size
        (4, None),
        (0, None),
    ]
)
def test_get_inner_width(width: int, result: int):
    panel = ReleasedPanelBase('test')
    if result is not None:
        assert panel._get_inner_width(width) == result
        return

    with pytest.raises(ValueError):
        panel._get_inner_width(width)


@pytest.mark.unit
@pytest.mark.parametrize(
    'style,result',
    [
        ('╭╮╰╯─│', BorderStyle('╭', '╮', '╰', '╯', '─', '│')),
        ('╭╮╰╯─', BorderStyle('╭', '╮', '╰', '╯', '─', '')),
        ('123456', BorderStyle('1', '2', '3', '4', '5', '6')),
        ('12345', BorderStyle('1', '2', '3', '4', '5', '')),
        (123, None),
        ('╭╮', None),
        ('╭╮╰╯─│{', None),
        (BorderStyle('╭', '╮', '╰', '╯', '─', '│'), BorderStyle('╭', '╮', '╰', '╯', '─', '│')),
        (BorderStyle('1', '2', '3', '4', '5', '6'), BorderStyle('1', '2', '3', '4', '5', '6')),
    ]
)
def test_parse_border_style(style: Union[str, BorderStyle], result: BorderStyle):
    panel = ReleasedPanelBase('test')
    if result is not None:
        assert panel._parse_border_style(style) == result
        return

    with pytest.raises(ValueError):
        panel._parse_border_style(style)


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,char,result',
    [
        ('TITLE', Align.left, '-', '- TITLE --'),
        ('TITLE', Align.center, '-', '- TITLE --'),
        ('TITLE', Align.right, '-', '-- TITLE -'),
    ]
)
def test_fill_header(title: str, align: Align, char: str, result: str):
    panel = ReleasedPanelBase('test')
    assert panel._fill_header(title, align=align, width=10, char=char) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,left,char,right,result',
    [
        ('TITLE', Align.left, '╭', '-', '╮', '╭- TITLE --╮'),
    ]
)
def test_get_header(title: str, align: Align, left: str, char: str, right: str, result: str):
    panel = ReleasedPanelBase('test')
    assert panel.get_header(title, align=align, width=12, left=left, char=char, right=right) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'line,width,char,indent,result',
    [
        ('test', 6, '|', '', '| test   |'),
        ('test', 6, '|', ' ', '|  test  |'),
        ('test', 6, '|', '-', '| -test  |'),
        ('test', 6, '1', '-', '1 -test  1'),
        ('test', 10, '|', ' ', '|  test      |'),
    ]
)
def test_fill(line: str, width: int, char: str, indent: str, result: str):
    panel = ReleasedPanelBase('test')
    assert panel.fill(line, width=width, char=char, indent=indent) == result
