import typer

server_app = typer.Typer(no_args_is_help=True)

@server_app.command(name="start")
def server_start():
    print("Server Start feature is not implemented yet")
