import typer
from typing_extensions import Annotated
from ibm_watsonx_orchestrate.cli.commands.login import login_controller

login_app = typer.Typer(no_args_is_help=True)

@login_app.command(name="login")
def login(
    apikey: Annotated[str, typer.Option("--apikey", "-a", help="WXO API Key")] = None,
    url: Annotated[
        str,
        typer.Option("--url", "-u", help="URL of the WXO instance you wish to access"),
    ] = None,
):
    login_controller.login(apikey=apikey, url=url)