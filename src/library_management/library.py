from library_management import book, user
app = Typer(name="library-management")
app.add_typer(user.app)
if __name__ == "__main__":
    app()
