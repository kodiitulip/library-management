from __future__ import annotations

import json
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

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(book_dict: dict) -> Book | None:
        if "title" not in book_dict:
            return None
        title, author = (
            book_dict.get("title", "MISSING"),
            book_dict.get("author", "MISSING"),
        )
        b = Book(title, author)
        b.status = book_dict.get("status", BookStatus.AVAILABLE)
        return b


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

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(node_dict: dict) -> BookNode | None:
        if not node_dict:
            return None
        if "book" not in node_dict:
            return None
        b = Book.from_dict(node_dict.get("book", {}))
        if not b:
            return None
        n = BookNode(b)
        n.left = BookNode.from_dict(node_dict.get("left", {}))
        n.right = BookNode.from_dict(node_dict.get("right", {}))
        n.amount = node_dict.get("amount", 0)
        return n


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
        self.to_file(self.__path)

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

    def to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.root.to_dict() if self.root else {}, f, indent=2)

    @staticmethod
    def from_file(path: str) -> BookBST:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        tree = BookBST(path)
        tree.root = BookNode.from_dict(data)
        return tree
