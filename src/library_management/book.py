from __future__ import annotations

from typer import Context, Option, Typer
from rich import print
from library_management.data import Book, BookBST


books = Typer(name="book")


@books.command("add")
def add_book(
    ctx: Context,
    title: str = Option(..., prompt=True),
    author: str = Option("Unknown/Anon", prompt=True),
):
    library: BookBST = ctx.obj.bst
    new_book: Book = Book(title, author)
    library.insert(new_book)
    print(f"Book of title: {new_book.title} added to the library\n\n")
    list_books(ctx)


@books.command("list")
def list_books(ctx: Context):
    b = ctx.obj.bst.in_order_traversal()
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")


@books.command("find")
def find_books(ctx: Context, name: str, author: bool = Option(False, "--author", "-a")):
    library: BookBST = ctx.obj.bst
    b: list[Book] = (
        library.list_by_author(name) if author else library.list_by_title(name)
    )
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")
