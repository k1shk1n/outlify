from typing import Union, Optional, Any

import pytest

from outlify.panel import PanelBase, Panel, ParamsPanel
from outlify.style import Align, BorderStyle, Style, AnsiStylesCodes


class ReleasedPanelBase(PanelBase):
    def __init__(
            self, content: str, *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            title_style: Union[str, Style] = 'reset',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            subtitle_style: Union[str, Style] = 'reset',
            border: Union[str | BorderStyle] = '╭╮╰╯─│'
    ):
        super().__init__(
            content, width=width,
            title=title, title_align=title_align, title_style=title_style,
            subtitle=subtitle, subtitle_align=subtitle_align, subtitle_style=subtitle_style,
            border=border
        )

    def get_content(self, content: str, *, width: int, char: str) -> str:
        return ''

RELEASED_RESET = '\033[0m'


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
    base = ReleasedPanelBase('test')
    if result is not None:
        assert base._get_inner_width(width) == result
        return

    with pytest.raises(ValueError):
        base._get_inner_width(width)


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
    base = ReleasedPanelBase('test')
    if result is not None:
        assert base._parse_border(style) == result
        return

    with pytest.raises(ValueError):
        base._parse_border(style)


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,char,result',
    [
        ('TITLE', Align.left, '-', f'- {RELEASED_RESET}TITLE{RELEASED_RESET} --'),
        ('TITLE', Align.center, '-', f'- {RELEASED_RESET}TITLE{RELEASED_RESET} --'),
        ('TITLE', Align.right, '-', f'-- {RELEASED_RESET}TITLE{RELEASED_RESET} -'),
    ]
)
def test_fill_header(title: str, align: Align, char: str, result: str):
    assert ReleasedPanelBase('test')._fill_header(
        title, align=align, width=10, char=char, title_style=Style(AnsiStylesCodes.reset)
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,left,char,right,result',
    [
        ('TITLE', Align.left, '╭', '-', '╮', f'╭- {RELEASED_RESET}TITLE{RELEASED_RESET} --╮'),
        ('TITLE', Align.center, '╭', '-', '╮', f'╭- {RELEASED_RESET}TITLE{RELEASED_RESET} --╮'),
        ('TITLE', Align.right, '╭', '-', '╮', f'╭-- {RELEASED_RESET}TITLE{RELEASED_RESET} -╮'),
        ('fake', Align.center, '╭', '-', '╮', f'╭-- {RELEASED_RESET}fake{RELEASED_RESET} --╮'),
        ('fake', Align.center, '+', ' ', '+', f'+   {RELEASED_RESET}fake{RELEASED_RESET}   +'),
    ]
)
def test_get_header(title: str, align: Align, left: str, char: str, right: str, result: str):
    base = ReleasedPanelBase('test')
    assert base.get_header(
        title, align=align, title_style=Style('reset'), width=12, left=left, char=char, right=right
    ) == result


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
    assert ReleasedPanelBase('test').fill(line, width=width, char=char, indent=indent) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'text,title,title_align,subtitle,subtitle_align,result',
    [
        (
            'test', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test             │\n'
            '╰──────────────────╯'
        ),
        (
            'test looooong text', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test looooong    │\n'
            '│ text             │\n'
            '╰──────────────────╯'
        ),
        (
            'test looooonooooooooog', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test looooonoooo │\n'
            '│ ooooog           │\n'
            '╰──────────────────╯'
        ),

        (
            'test', 'title1', 'left', 'title2', 'left',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ test             │\n╰'
            f'─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            'test', 'title1', 'center', 'title2', 'center',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ test             │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),

        (
            'test', 'title1', 'right', 'title2', 'right',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ test             │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),
        (
            'test', 'title1', 'left', 'title2', 'center',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ test             │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),
        (
            'test', 'title1', 'left', 'title2', 'right',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ test             │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),

        (
            'test', 'title1', 'center', 'title2', 'left',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ test             │\n'
            f'╰─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            'test', 'title1', 'center', 'title2', 'right',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ test             │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),

        (
            'test', 'title1', 'right', 'title2', 'left',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ test             │\n'
            f'╰─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            'test', 'title1', 'right', 'title2', 'center',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ test             │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),
    ]
)
def test_panel(text: str, title: str, title_align: str, subtitle: str, subtitle_align: str, result: str):
    panel = Panel(
        text, width=20, title=title, subtitle=subtitle,
        title_align=title_align, title_style='reset',
        subtitle_align=subtitle_align, subtitle_style='reset'
    )
    assert str(panel) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'params,title,title_align,subtitle,subtitle_align,result',
    [
        (
            {'x': 10, 'y': 20}, '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ x = 10           │\n'
            '│ y = 20           │\n'
            '╰──────────────────╯'
        ),
        (
            {'x': 10000000000000}, '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ x = 100000000000 │\n'
            '│     00           │\n'
            '╰──────────────────╯'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'left',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ x = 10           │\n'
            f'╰─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'center',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ x = 10           │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'right',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ x = 10           │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'center',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ x = 10           │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),
        (
            {'x': 10}, 'title1', 'left', 'title2', 'right',
            f'╭─ {RELEASED_RESET}title1{RELEASED_RESET} ─────────╮\n'
            f'│ x = 10           │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),

        (
            {'x': 10}, 'title1', 'center', 'title2', 'left',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ x = 10           │\n'
            f'╰─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'right',
            f'╭───── {RELEASED_RESET}title1{RELEASED_RESET} ─────╮\n'
            f'│ x = 10           │\n'
            f'╰───────── {RELEASED_RESET}title2{RELEASED_RESET} ─╯'
        ),

        (
            {'x': 10}, 'title1', 'right', 'title2', 'left',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ x = 10           │\n'
            f'╰─ {RELEASED_RESET}title2{RELEASED_RESET} ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'center',
            f'╭───────── {RELEASED_RESET}title1{RELEASED_RESET} ─╮\n'
            f'│ x = 10           │\n'
            f'╰───── {RELEASED_RESET}title2{RELEASED_RESET} ─────╯'
        ),
    ]
)
def test_params_panel(
        params: dict[Any, Any], title: str, title_align: str, subtitle: str, subtitle_align: str,
        result: str
):
    panel = ParamsPanel(
        params, width=20, title=title, subtitle=subtitle,
        title_align=title_align, title_style='reset',
        subtitle_align=subtitle_align, subtitle_style='reset'
    )
    assert str(panel) == result
