import typer

chat_app = typer.Typer(no_args_is_help=True)

@chat_app.command(name="start")
def chat_start():
    print("Chat Start feature is not implemented yet")
