from __future__ import annotations

from typer import Argument, Context, Option, Typer
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
@bookcmd.command("remove")
@savemutation
def remove_book(
    ctx: Context,
    title: str = Argument(help="Título do livro a ser removido"),
    author: str = Argument(help="Autor do livro a ser removido"),
):
    """Remove um livro da lista de livros disponíveis"""
    library: BookBST = ctx.obj.book_storage
    books: list[Book] = library.list_by_title(title)
    found: list[Book] = [
        book
        for book in books
        if book.title.lower() == title.strip().lower()
        and book.author.lower() == author.strip().lower()
    ]

    if not found:
        print(f"[red]Livro [yellow]{title} por {author}[/yellow] não encontrado![/red]")
        return
    library.delete(found[0])
    print(
        f"[green]Livro [yellow]{found[0].title} por {found[0].author}[/yellow] foi removido![/green]"
    )
    list_books(ctx)


@bookcmd.command("list")
def list_books(ctx: Context):
    """Lista todos os livros disponíveis na Biblioteca"""
    b = ctx.obj.book_storage.in_order_traversal()
    for book in b:
        print(f"- [green]{book.title}[/green] por [yellow]{book.author}[/yellow]")


@bookcmd.command("find")
def find_books(ctx: Context, name: str, author: bool = Option(False, "--author", "-a")):
    """Encontra um livro pelo titúlo ou pelo autor"""
    library: BookBST = ctx.obj.book_storage
    b: list[Book] = (
        library.list_by_author(name) if author else library.list_by_title(name)
    )
    for book in b:
        print(f"- [green]{book.title}[/green] by [yellow]{book.author}[/yellow]")
