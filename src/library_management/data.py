from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Protocol


class BookStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


@dataclass(order=True)
class Book:
    title: str
    author: str
    status: BookStatus = field(default=BookStatus.AVAILABLE, init=False)

@dataclass()
class Member:
    name: str


class TraversalCompareFunction(Protocol):
    def __call__(self, book: Book, /) -> bool: ...


@dataclass(order=True)
class BookNode:
    book: Book
    left: BookNode | None = None
    right: BookNode | None = None
    amount: int = field(default=0, init=False)

class BookBST:
    @property
    def root(self) -> BookNode | None:
        return self.__root

    @root.setter
    def root(self, value: BookNode | None):
        self.__root = value

    def __init__(self, path: str = "./library.json") -> None:
        self.__root: BookNode | None = None
        self.__path: str = path

    def insert(self, book: Book) -> None:
        def _insert(node: BookNode | None) -> BookNode | None:
            if not node:
                return BookNode(book)
            if book < node.book:
                node.left = _insert(node.left)
            elif book > node.book:
                node.right = _insert(node.right)
            else:
                node.amount += 1
                return node
            return node

        self.__root = _insert(self.root)
    def search_by_title(self, title: str) -> Book | None:
        def _search(node: BookNode | None) -> Book | None:
            if not node:
                return None
            if title == node.book.title:
                return node.book
            elif title < node.book.title:
                return _search(node.left)
            else:
                return _search(node.right)

        return _search(self.root)

    def in_order_traversal(
        self, compare_fn: TraversalCompareFunction = lambda _: True
    ) -> list[Book]:
        result: list[Book] = list()

        def _in_order(node: BookNode | None) -> None:
            if not node:
                return
            _in_order(node.left)
            if not compare_fn:
                raise ValueError("Compare function could not be called")
            elif compare_fn(node.book):
                result.append(node.book)
            _in_order(node.right)

        _in_order(self.root)
        return result

    def list_by_author(self, author: str) -> list[Book]:
        return self.in_order_traversal(
            lambda n: n.author.strip().lower() == author.lower()
        )

    def list_by_title(self, title: str) -> list[Book]:
        return self.in_order_traversal(
            lambda n: title.strip().lower() in n.title.lower()
        )

