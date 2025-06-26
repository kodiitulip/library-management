import os
from dataclasses import dataclass

from typer import Context, Typer, echo

from library_management.data import BookBST
from library_management.commands.book import bookcmd

app = Typer(name="library-management")
app.add_typer(bookcmd)


@dataclass
class State:
    book_storage: BookBST
    storage_path: str


@app.callback(invoke_without_command=True)
def main(ctx: Context):
    """Library Management CLI Tool"""
    path = os.getenv("LIBRARY_STORAGE_PATH", "library.json")
    if os.path.exists(path):
        book_storage = BookBST.from_file(path)
    else:
        book_storage = BookBST()
    ctx.obj = State(book_storage, path)
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())


@bookcmd.callback(invoke_without_command=True)
def book(ctx: Context):
    """Book Commands"""
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())


if __name__ == "__main__":
    app()
