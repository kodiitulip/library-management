from typer import Context, Option, Typer

from rich import print

from library_management.data import Member, MemberList
from library_management.hooks import savemutation

usercmd = Typer(name="user", help="Comandos para lidar com usuários")


@usercmd.command("list")
def list_users(ctx: Context):
    users: list[Member] = ctx.obj.member_storage.members
    print("\n".join(__get_pretty_list(users, ctx.obj.member_storage)))


def __get_pretty_list(
    member_list: list[Member], member_storage: MemberList
) -> list[str]:
    pretty_list = []
    if member_storage.logged_member is None:
        pretty_list.append("[red]Sem usuário ativo[/red]")
    for i, member in enumerate(member_list):
        active = member == member_storage.logged_member
        mstr = f"{i + 1}. [yellow]{member.username}[/yellow]" + (
            "\t[green](active)[/green]" if active else ""
        )
        pretty_list.append(mstr)
    return pretty_list


@usercmd.command("add")
@savemutation
def register_user(
    ctx: Context,
    username: str = Option(..., prompt=True),
    password: str = Option(..., prompt=True, hide_input=True),
):
    """Registra um novo usuário"""
    member_storage: MemberList = ctx.obj.member_storage
    member_storage.append(Member(username=username, password=password))
    print(f"[green]Added user [yellow]{username}[/yellow][/green]\n")


@usercmd.command("login")
@savemutation
def login_user(
    ctx: Context,
    username: str = Option(..., prompt=True),
    password: str = Option(..., prompt=True, hide_input=True),
):
    """Entrar na conta de usuário"""
    member_storage: MemberList = ctx.obj.member_storage
    exists, logged = member_storage.find(name=username, passwd=password)
    member_storage.logged_member = logged if exists else member_storage.logged_member
    msg = (
        f"[green]Boas vindas [yellow]{username}[/yellow][/green]"
        if exists
        else "[red]Usuário não encontrado[/red]"
    )
    print(msg)


@usercmd.command("logout")
@savemutation
def logout_user(ctx: Context) -> None:
    """Sair da conta atual"""
    member_storage: MemberList = ctx.obj.member_storage
    member_storage.logged_member = None
    print("logged out!")
