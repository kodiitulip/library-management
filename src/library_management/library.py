import os
from dataclasses import dataclass

from typer import Context, Typer

from library_management import book, user
from library_management.data import BookBST

app = Typer(name="library-management")
app.add_typer(user.app)
app.add_typer(book.books)


@dataclass
class State:
    bst: BookBST


@app.callback()
def main_callback(ctx: Context):
    ctx.obj = State(
        BookBST.from_file(os.getenv("LIBRARY_SOTRAGE_PATH") or "library.json")
    )


if __name__ == "__main__":
    app()
