from __future__ import annotations

from typer import Context, Option, Typer
from rich import print
from library_management.data import Book, BookBST
from library_management.hooks import savemutation

bookcmd = Typer(name="book")


@bookcmd.command("add")
@savemutation
def add_book(
    ctx: Context,
    title: str = Option(..., prompt=True),
    author: str = Option("Unknown/Anon", prompt=True),
):
    book: Book = Book(title, author)
    ctx.obj.book_storage.insert(book)
    print(f"Book of title: {book.title} added to the library\n\n")


@bookcmd.command("list")
def list_books(ctx: Context):
    b = ctx.obj.book_storage.in_order_traversal()
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")


@bookcmd.command("find")
def find_books(ctx: Context, name: str, author: bool = Option(False, "--author", "-a")):
    library: BookBST = ctx.obj.book_storage
    b: list[Book] = (
        library.list_by_author(name) if author else library.list_by_title(name)
    )
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")
