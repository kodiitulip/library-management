from __future__ import annotations
from typing import Any

import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
import os
from typing import Protocol


class BookStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


@dataclass
class State:
    book_storage: BookBST
    member_storage: MemberList
    lib_path: str
    member_path: str


@dataclass(order=True)
class Member:
    username: str
    password: str = field(compare=False)
    borrowed_books: list[Book] = field(default_factory=list, compare=False)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(dict: dict[str, Any]) -> Member:
        if "username" not in dict or "password" not in dict:
            raise ValueError("Could not parse user from dictionary")
        books = [Book.from_dict(book) for book in dict.get("borrowed_books", [])]
        borrowed = [book for book in books if book is not None]
        return Member(
            username=dict["username"],
            password=dict["password"],
            borrowed_books=borrowed,
        )


@dataclass
class MemberList:
    members: list[Member] = field(default_factory=list, kw_only=True)
    logged_member: Member | None = field(kw_only=True, default=None)

    def find(self, name: str, passwd: str) -> tuple[bool, Member | None]:
        try:
            idx = self.members.index(Member(name, passwd))
            return True, self.members[idx]
        except ValueError:
            return False, None

    def append(self, new_member: Member) -> None:
        self.members.append(new_member)
        self.members.sort()

    def to_file(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)

    @staticmethod
    def from_file(path: str):
        memlist = MemberList()
        if not os.path.exists(path):
            return memlist
        with open(path, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        members: list[dict[str, str]] = data.get("members", [])
        memlist.members = [Member.from_dict(member) for member in members]
        memlist.members.sort()
        logged = data.get("logged_member", {}) or {}
        memlist.logged_member = memlist.find(
            passwd=logged.get("password", ""), name=logged.get("username", "")
        )[1]
        return memlist


@dataclass(order=True, unsafe_hash=True)
class Book:
    title: str
    author: str
    status: BookStatus = field(default=BookStatus.AVAILABLE, init=False, compare=False)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(book_dict: dict) -> Book | None:
        if "title" not in book_dict:
            return None
        title, author = (
            book_dict["title"],
            book_dict.get("author", "MISSING"),
        )
        b = Book(title, author)
        status = book_dict.get("status", BookStatus.AVAILABLE)
        b.status = BookStatus(status)
        return b


@dataclass(order=True)
class BookNode:
    book: Book
    left: BookNode | None = field(default=None, kw_only=True, compare=False)
    right: BookNode | None = field(default=None, kw_only=True, compare=False)
    amount: int = field(default=1, init=False, compare=False)

    def to_dict(self) -> dict:
        return asdict(self)
        # return {
        #     "book": self.book.to_dict(),
        #     "left": self.left.to_dict() if self.left else None,
        #     "right": self.right.to_dict() if self.right else None,
        #     "parent": self.parent.to_dict() if self.parent else None,
        #     "amount": self.amount,
        # }

    @staticmethod
    def from_dict(node_dict: dict) -> BookNode | None:
        if not node_dict or "book" not in node_dict:
            return None
        b = Book.from_dict(node_dict.get("book", {}))
        if not b:
            return None
        n = BookNode(b)
        n.left = BookNode.from_dict(node_dict.get("left", {}))
        n.right = BookNode.from_dict(node_dict.get("right", {}))
        n.amount = node_dict.get("amount", 1)
        return n

    def successor(self) -> BookNode:
        """grabs the lowest value that's greater than <self>"""
        right = self.right
        if right is None:
            return self

        current = right
        while current.left is not None:
            current = current.left
        return current


class BookBST:
    class TraversalCompareFunction(Protocol):
        def __call__(self, book: Book, /) -> bool: ...

    @property
    def root(self) -> BookNode | None:
        return self.__root

    @root.setter
    def root(self, value: BookNode | None):
        self.__root = value

    def __init__(self) -> None:
        self.__root: BookNode | None = None

    def insert(self, book: Book) -> None:
        def _insert(node: BookNode | None) -> BookNode:
            if node is None:
                return BookNode(book)
            elif book < node.book:
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
            if title.strip().lower() == node.book.title.lower():
                return node.book
            elif title < node.book.title:
                return _search(node.left)
            else:
                return _search(node.right)

        return _search(self.root)

    def search_by_book(self, book: Book) -> tuple[bool, BookNode]:
        node = BookNode(book=book)
        if self.root is None:
            return False, node

        def _search(root: BookNode | None) -> tuple[bool, BookNode]:
            if root is None:
                return False, node
            elif root == node:
                return True, root
            elif root < node:
                return _search(root.left)
            else:
                return _search(root.right)

        return _search(self.root)

    def delete(self, book: Book) -> None:
        exists, _ = self.search_by_book(book)

        if not exists:
            print(f"[red]Livro {book.title} por {book.author} não encontrado![/red]")
            return

        def _delete(root: BookNode | None, key: Book) -> BookNode | None:
            if root is None:
                return root
            if key < root.book:
                root.left = _delete(root.left, key)
            elif key > root.book:
                root.right = _delete(root.right, key)
            else:
                if root.left is None:
                    return root.right
                elif root.right is None:
                    return root.left
                else:
                    succ = root.successor()
                    root.book = succ.book
                    root.right = _delete(root.right, succ.book)
            return root

        self.__root = _delete(self.root, book)

    def in_order_traversal(
        self, compare_fn: TraversalCompareFunction = lambda _: True
    ) -> list[Book]:
        result: list[Book] = list()

        def _in_order(node: BookNode | None) -> None:
            if not node:
                return
            _in_order(node.left)
            if compare_fn(node.book):
                result.append(node.book)
            _in_order(node.right)

        _in_order(self.root)
        return result

    def list_by_author_and_title(self, title: str, author: str) -> list[Book]:
        by_author = set(self.list_by_author(author))
        by_title = set(self.list_by_title(title))
        return list(by_author.intersection(by_title))

    def list_by_author(self, author: str) -> list[Book]:
        return self.in_order_traversal(
            lambda n: author.strip().lower() in n.author.lower()
        )

    def list_by_title(self, title: str) -> list[Book]:
        return self.in_order_traversal(
            lambda n: title.strip().lower() in n.title.lower()
        )

    def __len__(self) -> int:
        return len(self.in_order_traversal())

    def __contains__(self, title: str) -> bool:
        return self.search_by_title(title) is not None

    def to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.root.to_dict() if self.root else {}, f, indent=2)

    @staticmethod
    def from_file(path: str) -> BookBST:
        tree = BookBST()
        if not os.path.exists(path):
            return tree
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        tree.root = BookNode.from_dict(data)
        return tree
