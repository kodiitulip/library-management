from typer import Context, Option, Typer

from rich import print

from library_management.data import Member, MemberList, BookBST, BookStatus
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

@usercmd.command("borrow")
@savemutation
def borrow_book(
    ctx: Context, 
    title: str = Option(..., "--title", "-t", prompt=True)
):
    """Pegar um livro emprestado"""
    member_storage: MemberList = ctx.obj.member_storage
    book_storage: BookBST = ctx.obj.book_storage
    member = member_storage.logged_member
    
    if member is None:
        print("[red]Você precisa estar logado para emprestar livros[/red]")
        return

    book = book_storage.search_by_title(title)
    if book is None:
        print(f"[red]Livro '{title}' não encontrado[/red]")
        return

    if book.status == BookStatus.UNAVAILABLE:
        print(f"[red]Livro '{title}' já está emprestado[/red]")
        return

    book.status = BookStatus.UNAVAILABLE
    member.borrowed_books.append(book.title)
    print(f"[green]Livro '{title}' emprestado para {member.username}[/green]")

@usercmd.command("return")
@savemutation
def return_book(
    ctx: Context, 
    title: str = Option(..., "--title", "-t", prompt=True)
):
    """Devolver um livro emprestado"""
    member_storage: MemberList = ctx.obj.member_storage
    book_storage: BookBST = ctx.obj.book_storage
    member = member_storage.logged_member
    
    if member is None:
        print("[red]Você precisa estar logado para devolver livros[/red]")
        return

    if title not in member.borrowed_books:
        print(f"[red]Você não tem o livro '{title}' emprestado[/red]")
        return

    book = book_storage.search_by_title(title)
    if book is None:
        print(f"[red]Livro '{title}' não encontrado[/red]")
        return

    book.status = BookStatus.AVAILABLE
    member.borrowed_books.remove(title)
    print(f"[green]Livro '{title}' devolvido por {member.username}[/green]")


@usercmd.command("track")
def list_borrowed_books(ctx: Context):
    """Lista os livros emprestados pelo usuário logado"""
    member_storage: MemberList = ctx.obj.member_storage
    member = member_storage.logged_member
    
    if member is None:
        print("[red]Você precisa estar logado para ver seus livros emprestados[/red]")
        return

    if not member.borrowed_books:
        print("[yellow]Você não tem livros emprestados[/yellow]")
        return

    print(f"[green]Livros emprestados para {member.username}:[/green]")
    for book in member.borrowed_books:
        print(f"- {book}")

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

