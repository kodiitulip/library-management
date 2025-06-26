from typer import Option, Typer

from rich import print

from library_management.data import Member
from library_management.cli import app

user = Typer(name="user", no_args_is_help=True)
app.add_typer(user)

USERS: list[Member] = []


@user.command("list")
def list_users():
    print("\n".join([f"[yellow]{i.name}[/yellow]" for i in USERS]))


@user.command("add")
def register_user(
    username: str = Option(..., prompt=True),
):
    USERS.append(Member(username))
    print(f"[green]Added user [yellow]{username}[/yellow][/green]\n")
    list_users()
