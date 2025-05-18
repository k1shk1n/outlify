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
            border=border, border_style='reset'
        )

    def get_content(self, content: str, *, width: int, char: str, border_style: Style) -> str:
        return ''

RESET = '\033[0m'


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
        ('TITLE', Align.left, '-', f'-{RESET} {RESET}TITLE{RESET} {RESET}--'),
        ('TITLE', Align.center, '-', f'-{RESET} {RESET}TITLE{RESET} {RESET}--'),
        ('TITLE', Align.right, '-', f'--{RESET} {RESET}TITLE{RESET} {RESET}-'),
    ]
)
def test_fill_header(title: str, align: Align, char: str, result: str):
    assert ReleasedPanelBase('test')._fill_header(
        title, align=align, width=10, char=char,
        title_style=Style(AnsiStylesCodes.reset), border_style=Style(AnsiStylesCodes.reset)
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,left,char,right,result',
    [
        ('TITLE', Align.left, '╭', '-', '╮', f'{RESET}╭-{RESET} {RESET}TITLE{RESET} {RESET}--╮{RESET}'),
        ('TITLE', Align.center, '╭', '-', '╮', f'{RESET}╭-{RESET} {RESET}TITLE{RESET} {RESET}--╮{RESET}'),
        ('TITLE', Align.right, '╭', '-', '╮', f'{RESET}╭--{RESET} {RESET}TITLE{RESET} {RESET}-╮{RESET}'),
        ('fake', Align.center, '╭', '-', '╮', f'{RESET}╭--{RESET} {RESET}fake{RESET} {RESET}--╮{RESET}'),
        ('fake', Align.center, '+', ' ', '+', f'{RESET}+  {RESET} {RESET}fake{RESET} {RESET}  +{RESET}'),
    ]
)
def test_get_header(title: str, align: Align, left: str, char: str, right: str, result: str):
    base = ReleasedPanelBase('test')
    assert base.get_header(
        title, align=align, title_style=Style(AnsiStylesCodes.reset), width=12, left=left, char=char, right=right,
        border_style=Style(AnsiStylesCodes.reset)
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'line,width,char,indent,result',
    [
        ('test', 6, '|', '', f'{RESET}|{RESET} test   {RESET}|{RESET}'),
        ('test', 6, '|', ' ', f'{RESET}|{RESET}  test  {RESET}|{RESET}'),
        ('test', 6, '|', '-', f'{RESET}|{RESET} -test  {RESET}|{RESET}'),
        ('test', 6, '1', '-', f'{RESET}1{RESET} -test  {RESET}1{RESET}'),
        ('test', 10, '|', ' ', f'{RESET}|{RESET}  test      {RESET}|{RESET}'),
    ]
)
def test_fill(line: str, width: int, char: str, indent: str, result: str):
    assert ReleasedPanelBase('test').fill(
        line, width=width, char=char, indent=indent, border_style=Style(AnsiStylesCodes.reset)
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'text,title,title_align,subtitle,subtitle_align,result',
    [
        (
            'test', '', 'center', '', 'center',
            f'{RESET}╭──────────────────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰──────────────────╯{RESET}'
        ),
        (
            'test looooong text', '', 'center', '', 'center',
            f'{RESET}╭──────────────────╮{RESET}\n'
            f'{RESET}│{RESET} test looooong    {RESET}│{RESET}\n'
            f'{RESET}│{RESET} text             {RESET}│{RESET}\n'
            f'{RESET}╰──────────────────╯{RESET}'
        ),
        (
            'test looooonooooooooog', '', 'center', '', 'center',
            f'{RESET}╭──────────────────╮{RESET}\n'
            f'{RESET}│{RESET} test looooonoooo {RESET}│{RESET}\n'
            f'{RESET}│{RESET} ooooog           {RESET}│{RESET}\n'
            f'{RESET}╰──────────────────╯{RESET}'
        ),

        (
            'test', 'title1', 'left', 'title2', 'left',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            'test', 'title1', 'center', 'title2', 'center',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
        ),

        (
            'test', 'title1', 'right', 'title2', 'right',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),
        (
            'test', 'title1', 'left', 'title2', 'center',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
        ),
        (
            'test', 'title1', 'left', 'title2', 'right',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),

        (
            'test', 'title1', 'center', 'title2', 'left',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            'test', 'title1', 'center', 'title2', 'right',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),

        (
            'test', 'title1', 'right', 'title2', 'left',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            'test', 'title1', 'right', 'title2', 'center',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} test             {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
        ),
    ]
)
def test_panel(text: str, title: str, title_align: str, subtitle: str, subtitle_align: str, result: str):
    panel = Panel(
        text, width=20, title=title, subtitle=subtitle,
        title_align=title_align, title_style='reset',
        subtitle_align=subtitle_align, subtitle_style='reset',
        border_style='reset'
    )
    assert str(panel) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'params,title,title_align,subtitle,subtitle_align,result',
    [
        (
            {'x': 10, 'y': 20}, '', 'center', '', 'center',
            f'{RESET}╭──────────────────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}│{RESET} y = 20           {RESET}│{RESET}\n'
            f'{RESET}╰──────────────────╯{RESET}'
        ),
        (
            {'x': 10000000000000}, '', 'center', '', 'center',
            f'{RESET}╭──────────────────╮{RESET}\n'
            f'{RESET}│{RESET} x = 100000000000 {RESET}│{RESET}\n'
            f'{RESET}│{RESET}     00           {RESET}│{RESET}\n'
            f'{RESET}╰──────────────────╯{RESET}'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'left',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'center',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'right',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'center',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
        ),
        (
            {'x': 10}, 'title1', 'left', 'title2', 'right',
            f'{RESET}╭─{RESET} {RESET}title1{RESET} {RESET}─────────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),

        (
            {'x': 10}, 'title1', 'center', 'title2', 'left',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'right',
            f'{RESET}╭─────{RESET} {RESET}title1{RESET} {RESET}─────╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────────{RESET} {RESET}title2{RESET} {RESET}─╯{RESET}'
        ),

        (
            {'x': 10}, 'title1', 'right', 'title2', 'left',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─{RESET} {RESET}title2{RESET} {RESET}─────────╯{RESET}'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'center',
            f'{RESET}╭─────────{RESET} {RESET}title1{RESET} {RESET}─╮{RESET}\n'
            f'{RESET}│{RESET} x = 10           {RESET}│{RESET}\n'
            f'{RESET}╰─────{RESET} {RESET}title2{RESET} {RESET}─────╯{RESET}'
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
        subtitle_align=subtitle_align, subtitle_style='reset',
        border_style='reset'
    )
    assert str(panel) == result
