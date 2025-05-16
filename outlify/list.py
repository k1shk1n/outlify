from abc import ABC, abstractmethod
from typing import Sequence, Any, Optional

from outlify._utils import resolve_width


__all__ = ['TitledList']


class ListBase(ABC):

    def __init__(self, content: Sequence[Any], *, width: Optional[int], title: str, title_separator: str):
        self.width = resolve_width(width)
        self.title = self._get_title(title, len(content))
        self.title_separator = title_separator

        content = self._prepare_content(content)
        self.content = self.get_content(content, width=self.width)

    @abstractmethod
    def get_content(self, content: list[Any], *, width: int) -> str:
        pass

    @staticmethod
    def _get_title(title: str, count: int) -> str:
        return f'{title} ({count})'

    @staticmethod
    def _prepare_content(content: Sequence[Any]) -> list[str]:
        return [str(elem) for elem in content]

    def __str__(self) -> str:
        if len(self.content) == 0:
            return self.title
        return self.title_separator.join((self.title, self.content))

    def __repr__(self) -> str:
        return self.__str__()


class TitledList(ListBase):

    def __init__(
            self, content: Sequence[Any], *, title: str = 'Content',
            separator: str = '  '
    ):
        self.separator = separator
        super().__init__(content, width=None, title=title, title_separator=': ')

    def get_content(self, content: list[str], *, width: int) -> str:
        return self.separator.join(content)


if __name__ == '__main__':
    print(
        'Outlify helps you create list output in a beautiful format\n',
        'The first one is the simplest: a titled list', sep='\n'
    )
    print(TitledList(['ruff@1.0.0', 'pytest@1.2.3', 'mkdocs@3.2.1', 'mike@0.0.1'], title='Packages'))
