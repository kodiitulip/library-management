from __future__ import annotations

from typer import Context, Option, Typer
from rich import print
from library_management.data import Book, BookBST
from library_management.hooks import savemutation

bookcmd = Typer(name="book", help="Comandos relacionados a gerenciamendo de livros")


@bookcmd.command("donate")
@savemutation
def add_book(
    ctx: Context,
    title: str = Option(..., "--title", "-t", prompt=True),
    author: str = Option("Unknown/Anon", "--author", "-a", "--by", prompt=True),
):
    """Adiciona um livro a lista da Bilioteca"""
    book: Book = Book(title, author)
    ctx.obj.book_storage.insert(book)
    print(f"Book of title: {book.title} added to the library\n\n")


@bookcmd.command("list")
def list_books(ctx: Context):
    """Lista todos os livros disponíveis na Biblioteca"""
    b = ctx.obj.book_storage.in_order_traversal()
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")


@bookcmd.command("find")
def find_books(ctx: Context, name: str, author: bool = Option(False, "--author", "-a")):
    """Encontra um livro pelo titúlo ou pelo autor"""
    library: BookBST = ctx.obj.book_storage
    b: list[Book] = (
        library.list_by_author(name) if author else library.list_by_title(name)
    )
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")
