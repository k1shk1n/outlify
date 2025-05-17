from abc import ABC, abstractmethod
from typing import Any, Mapping, Iterable, Optional, Union
import textwrap

from outlify.style import Align, BorderStyle, Style, AnsiStylesCodes
from outlify._utils import resolve_width, parse_title_align, parse_style
from outlify._ansi import wrap


__all__ = ['Panel', 'ParamsPanel']


RESET = Style(AnsiStylesCodes.reset)


class PanelBase(ABC):
    def __init__(
            self, content: Any, *, width: Optional[int],
            title: str, title_align: Union[str, Align], title_style: Union[str, Style],
            subtitle: str, subtitle_align: Union[str, Align], subtitle_style: Union[str, Style],
            border: Union[str | BorderStyle], border_style: Union[str, Style]
    ):
        border = self._parse_border(border)
        width = resolve_width(width)
        title_style, subtitle_style = parse_style(title_style), parse_style(subtitle_style)
        border_style = parse_style(border_style)
        self.header = self.get_header(
            title, align=parse_title_align(title_align), title_style=title_style, width=width,
            left=border.lt, char=border.headers, right=border.rt, border_style=border_style
        )
        self.footer = self.get_header(
            subtitle, align=parse_title_align(subtitle_align), title_style=subtitle_style, width=width,
            left=border.lb, char=border.headers, right=border.rb, border_style=border_style
        )
        self.content = self.get_content(content, width=width, char=border.sides, border_style=border_style)

    @abstractmethod
    def get_content(self, content: str, *, width: int, char: str, border_style: Style) -> str:
        pass

    @staticmethod
    def _get_inner_width(outside: int) -> int:
        """ Get inner panel width

        :param outside: outside panel width
        :return: inner panel width
        """
        if outside <= 4:
            raise ValueError(f'Invalid value for width: {outside} < 4')
        return outside - 4

    @staticmethod
    def _parse_border(style: str) -> BorderStyle:
        if isinstance(style, BorderStyle):
            return style
        if not isinstance(style, str):
            raise ValueError(
                f'Invalid type for border: {style} ({type(style)}) variable is not str or BorderStyle'
            )
        if len(style) not in [5, 6]:
            raise ValueError(f'Invalid length for border (!= 5 or != 6): length of {style} = {len(style)}')
        return BorderStyle(
            lt=style[0], rt=style[1],
            lb=style[2], rb=style[3],
            headers=style[4], sides=style[5] if len(style) == 6 else '',
        )

    def get_header(
            self, title: str, *, width: int, align: Align, title_style: Style,
            left: str, char: str, right: str, border_style: Style
    ) -> str:
        header = self._fill_header(
            title, width=width - 2, align=align, title_style=title_style,
            char=char, border_style=border_style
        )
        return f'{border_style}{left}{header}{right}{RESET}'

    @staticmethod
    def _fill_header(
            title: str, *, width: int, align: Align, title_style: Style,
            char: str, border_style: Style
    ) -> str:
        if title != '':
            width += len(str(title_style)) + len(RESET)   # title styling
            width += len(str(border_style)) + len(RESET)  # border styling
            title = f'{RESET} {wrap(title, title_style)} {border_style}'

        if align == Align.left:
            title = f'{char}{title}'
            return f'{title.ljust(width, char)}'
        elif align == Align.center:
            return title.center(width, char)
        title = f'{title}{char}'
        return title.rjust(width, char)

    @staticmethod
    def fill(line: str, *, width: int, char: str, border_style: Style, indent: str = '') -> str:
        """ Fill a single line

        :param line: the content to be placed inside the panel
        :param width: total available width for the content (excluding side borders)
        :param char: border character to be placed on both sides of the line
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        :param indent: indentation added before the content
        :return: a string representing the line wrapped with borders and padded to match the specified width
        """
        return f'{border_style}{char}{RESET} {indent}{line.ljust(width - len(indent))} {border_style}{char}{RESET}'

    def __str__(self) -> str:
        return '\n'.join([self.header, self.content, self.footer])

    def __repr__(self) -> str:
        return self.__str__()


class Panel(PanelBase):
    def __init__(
            self, content: str, *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            title_style: Union[str, Style] = 'default_color default_style',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            subtitle_style: Union[str, Style] = 'default_color default_style',
            border: Union[str | BorderStyle] = '╭╮╰╯─│',
            border_style: Union[str, Style] = 'default_color default_style',
    ):
        """ A simple panel for displaying plain text with customizable borders, title, and subtitle.

        This class inherits from `PanelBase` and provides a way to create a terminal panel with
        plain text content. It allows you to configure the panel's width, title, subtitle, alignment,
        and border style. The panel is designed to be used directly in the terminal for displaying information
        in a visually appealing way.

        :param content: the plain text content to be displayed inside the panel. It supports multi-line strings.
        :param width: total panel width (including borders)
        :param title: title displayed at the top of the panel
        :param title_align: alignment of the title. Can be a string ('left', 'center', 'right') or an Align enum/type
        :param title_style: ANSI style to apply to the title. Can be a string (e.g., 'red bold') or a `Style` instance.
                            Allows customization of title color and text style (e.g., bold, underline).
        :param subtitle: subtitle displayed below the title
        :param subtitle_align: alignment of the subtitle. Same format as title_align
        :param subtitle_style: ANSI style to apply to the subtitle. Can be a string (e.g., 'red bold') or a `Style`
                               instance. Allows customization of subtitle color and text style (e.g., bold, underline).
        :param border: Border character style. Can be a string representing custom border characters
                       or an instance of BorderStyle
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        """
        super().__init__(
            content, width=width,
            title=title, title_align=title_align, title_style=title_style,
            subtitle=subtitle, subtitle_align=subtitle_align, subtitle_style=subtitle_style,
            border=border, border_style=border_style
        )

    def get_content(self, content: str, *, width: int, char: str, border_style: Style) -> str:
        """ Get prepared panel content

        :param content: multi-line string to display in the panel
        :param width: total panel width (including borders)
        :param char: character for the side borders. If empty string, disables wrapping and borders
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        :return: panel with prepared content
        """
        if not isinstance(content, str):
            raise ValueError(f'Invalid type for content: {type(content)} is not str')
        width = self._get_inner_width(width)

        lines = []
        for line in content.splitlines():
            if char == '' or (line := line.strip()) == '':
                lines.append(line)
                continue

            wrapped = textwrap.wrap(
                line, width=width, replace_whitespace=False,
                drop_whitespace=False, break_on_hyphens=False
            )
            lines.extend(wrapped)

        lines = [self.fill(line, width=width, char=char, border_style=border_style) for line in lines]
        return '\n'.join(lines)


class ParamsPanel(PanelBase):
    def __init__(
            self, content: Mapping[Any, Any], *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            title_style: Union[str, Style] = 'default_color default_style',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            subtitle_style: Union[str, Style] = 'default_color default_style',
            border: Union[str | BorderStyle] = '╭╮╰╯─│',
            border_style: Union[str, Style] = 'default_color default_style',
            hidden: Iterable[str] = (), separator: str = ' = '
    ):
        """ A panel for displaying key-value parameters in a formatted layout.

        Inherits from `PanelBase` and is used to present a set of parameters, e.g. configuration settings,
        metadata, etc. in a styled, optionally bordered panel. Supports custom title, subtitle, alignment,
        and the ability to hide selected parameters.

        :param content: a mapping of keys to string values to display in the panel.
                        For example: {'learning_rate': '0.001', 'batch_size': '64'}.
        :param width: total panel width (including borders)
        :param title: title displayed at the top of the panel
        :param title_align: alignment of the title. Can be a string ('left', 'center', 'right') or an Align enum/type
        :param title_style: ANSI style to apply to the title. Can be a string (e.g., 'red bold') or a `Style` instance.
                            Allows customization of title color and text style (e.g., bold, underline).
        :param subtitle: subtitle displayed below the title
        :param subtitle_align: alignment of the subtitle. Same format as title_align
        :param subtitle_style: ANSI style to apply to the subtitle. Can be a string (e.g., 'red bold') or a `Style`
                               instance. Allows customization of subtitle color and text style (e.g., bold, underline).
        :param border: Border character style. Can be a string representing custom border characters
                       or an instance of BorderStyle
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        :param hidden: Iterable of keys from `content` that should be excluded from display.
                       Useful for filtering out sensitive or irrelevant data
        :param separator: key-value separator
        """
        self.hidden = hidden
        self.separator = separator
        super().__init__(
            content, width=width,
            title=title, title_align=title_align, title_style=title_style,
            subtitle=subtitle, subtitle_align=subtitle_align, subtitle_style=subtitle_style,
            border=border, border_style=border_style
        )

    def get_content(self, content: Mapping[Any, Any], *, width: int, char: str, border_style: Style) -> str:
        """ Get prepared panel content

        :param content: parameters that should be in the panel
        :param width: total panel width (including borders)
        :param char: character for the side borders. If empty string, disables wrapping and borders
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        :return: panel with prepared content
        """
        if not isinstance(content, Mapping):
            raise ValueError(f'Invalid type for content: {type(content)} is not Mapping')
        width = self._get_inner_width(width)
        params = self._prepare_params(content)

        lines = []
        max_key_length = max(len(key) for key in params.keys())
        width_inside = width - max_key_length - len(self.separator)
        indent = ' ' * (max_key_length + len(self.separator))
        for key, value in params.items():
            displayed_value = self._mask_value(key, value)
            line = f"{key.ljust(max_key_length)}{self.separator}{displayed_value}"

            if not char:  # mode without border in sides
                lines.append(f'  {line}')
            elif len(line) <= width:  # the whole line fits in the panel
                lines.append(self.fill(line, width=width, char=char, border_style=border_style))
            else:  # it's necessary to split the string
                lines.extend(self._wrap_line(line, width, width_inside, char, border_style, indent))
        return '\n'.join(lines)

    @staticmethod
    def _prepare_params(content: Mapping[Any, Any]) -> dict[str, str]:
        """ Converts all keys and values in the mapping to strings

        :param content: original content mapping
        :return: dictionary with stringified keys and values
        """
        return {str(key): str(value) for key, value in content.items()}

    def _mask_value(self, key: str, value: str) -> str:
        """ Replaces value with asterisks if the key is in the hidden list

        :param key: parameter name
        :param value: parameter value
        :return: either the original value or a masked string.
        """
        return "*****" if key in self.hidden else value

    def _wrap_line(
            self, line: str, width: int, width_inside: int, char: str, border_style: Style, indent: str
    ) -> list[str]:
        """ Wraps a long line into multiple lines with proper indentation and border formatting

        :param line: the full line to wrap
        :param width: full panel width including borders
        :param width_inside: usable width after the key and separator
        :param char: border character
        :param border_style: ANSI style to apply to the border. Can be a string (e.g., 'red bold') or a `Style`
                             instance. Allows customization of border color and text style (e.g., bold, underline).
        :param indent: indentation for wrapped lines
        :return: list of wrapped and formatted lines
        """
        head, tail = line[:width], line[width:]
        wrapped = textwrap.wrap(
            tail, width=width_inside, replace_whitespace=False,
            drop_whitespace=False, break_on_hyphens=False
        )
        lines = [self.fill(head, width=width, char=char, border_style=border_style)]
        lines.extend(
            self.fill(part, width=width, char=char, border_style=border_style, indent=indent) for part in wrapped
        )
        return lines


if __name__ == '__main__':
    text = (
        "Outlify helps you render beautiful command-line panels.\n"
        "You can customize borders, alignment, etc.\n\n"
        "This is just a simple text panel."
    )
    print(Panel(
        text, title='Welcome to Outlify', subtitle='Text Panel Demo', title_align='left', subtitle_align='right'
    ), '', sep='\n')

    long_text = (
        "In a world where CLI tools are often boring and unstructured, "
        "Outlify brings beauty and structure to your terminal output. "
        "It allows developers to create elegant panels with customizable borders, titles, subtitles, "
        "and aligned content — all directly in the terminal.\n\n"
        "Outlify is lightweight and dependency-free — it uses only Python’s standard libraries, "
        "so you can easily integrate it into any project without worrying about bloat or compatibility issues.\n\n"
        "Whether you're building debugging tools, reporting pipelines, or just want to print data in a cleaner way, "
        "Outlify helps you do it with style."
    )
    print(Panel(
        long_text, title='Long Text Panel Example', subtitle='using another border style', border='╔╗╚╝═║'
    ), '', sep='\n')

    text = (
        'or maybe you want to output parameters that came to your CLI input, '
        'but you do not want to output it in raw form or write a nice wrapper yourself, '
        'and the sensitive data should not be visible in the terminal, but you want to know that it is specified'
    )
    print(Panel(text, subtitle='See ↓ below', border='┌┐└┘  '), '', sep='\n')
    parameters = {
        'first name': 'Vladislav',
        'last name': 'Kishkin',
        'username': 'k1shk1n',
        'password': 'fake-password',
        'description': 'This is a fake description to show you how Outlify can wrap text in the Parameters Panel'
    }
    print(ParamsPanel(
        parameters, title='Start Parameters', hidden=('password',), title_style='default_color bold red', border_style='red'
    ))
