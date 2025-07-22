from __future__ import annotations

from rich.console import Console
from rich.table import Table
from typer import Argument, Context, Option, Typer
from rich import print
from library_management.data import Book, BookBST, BookStatus
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
    print(
        f"Livro [yellow]{book.title} por {book.author}[/yellow] foi adicionado a Biblioteca"
    )


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
    books: list[Book] = ctx.obj.book_storage.in_order_traversal()
    console = Console()
    table = Table("Título", "Autor", "Disponível", title="Tabela de Livros")
    for book in books:
        available = "[green]DISPONÍVEL[/green]" if book.status == BookStatus.AVAILABLE else "[red]INDISPONÍVEL[/red]"
        table.add_row(book.title, book.author, available)
    console.print(table)


@bookcmd.command("find")
def find_books(
    ctx: Context,
    title: str = Option("", "--title", "-t", help="Pesquisa por título", prompt=True),
    author: str = Option("", "--author", "-a", "--by", help="Pesquisa por autor", prompt=True),
):
    """Encontra um livro pelo titúlo ou pelo autor"""

    library: BookBST = ctx.obj.book_storage
    list_by_author = set( library.list_by_author(author) )
    list_by_title = set( library.list_by_title(title) )
    final = list(list_by_author.intersection(list_by_title))
    if not final:
        return print("[red]Livros não encontrados[/red]")
    console = Console()
    table = Table("Título", "Autor", "Disponível", title="Tabela de Livros")
    for book in final:
        available = "[green]DISPONÍVEL[/green]" if book.status == BookStatus.AVAILABLE else "[red]INDISPONÍVEL[/red]"
        table.add_row(book.title, book.author, available)
    console.print(table)
