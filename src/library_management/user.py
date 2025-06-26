from typer import Option, Typer

from rich import print

from library_management.data import Member

app = Typer(name="user", no_args_is_help=True)


USERS: list[Member] = []


@app.command("list")
def list_users():
    print("\n".join([f"[yellow]{i.name}[/yellow]" for i in USERS]))


@app.command("add")
def register_user(
    username: str = Option(..., prompt=True),
):
    USERS.append(Member(username))
    print(f"[green]Added user [yellow]{username}[/yellow][/green]\n")
    list_users()
