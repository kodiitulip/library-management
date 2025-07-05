import os

from typer import Context, Typer, echo

from library_management.commands.user import usercmd
from library_management.data import BookBST, MemberList, State
from library_management.commands.book import bookcmd

app = Typer(
    name="library-management",
    help="Ferramenta de comando para gerenciar uma biblioteca",
)
app.add_typer(bookcmd)
app.add_typer(usercmd)


@app.callback(invoke_without_command=True)
def main(ctx: Context):
    """Callback para carregar o arquivo de memória e chamar ajuda quando faltar subcommandos"""
    try:
        os.makedirs(os.getenv("LIBRARY_STORAGE_DIR", "gendata/"))
    except OSError:
        pass
    lib_path = os.getenv("LIBRARY_STORAGE_PATH", "gendata/library.json")
    member_path = os.getenv("MEMBER_STORAGE_PATH", "gendata/members.json")
    book_storage = BookBST.from_file(lib_path)
    member_storage = MemberList.from_file(member_path)
    ctx.obj = State(
        book_storage=book_storage,
        member_storage=member_storage,
        lib_path=lib_path,
        member_path=member_path,
    )
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())


@usercmd.callback(invoke_without_command=True)
@bookcmd.callback(invoke_without_command=True)
def no_args_help(ctx: Context):
    """Callback para chamar --help quando não tiver subcomandos"""
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())


if __name__ == "__main__":
    app()
