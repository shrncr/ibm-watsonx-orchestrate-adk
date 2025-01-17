import typer
from typing_extensions import Annotated
from ibm_watsonx_orchestrate.cli.commands.tools import tools_controller
tools_app= typer.Typer(no_args_is_help=True)

@tools_app.command(name="import")
def tool_import(
    kind: Annotated[
        tools_controller.ToolKind,
        typer.Option("--kind", "-k", help="Import Source Format"),
    ],
    file: Annotated[
        str,
        typer.Option(
            "--file",
            "-f",
            help="Path to Python or OpenAPI spec YAML file. Required for kind openapi or python",
        ),
    ] = None,
    skillset_id: Annotated[
        str, typer.Option("--skillset_id", help="ID of skill set in WXO")
    ] = None,
    skill_id: Annotated[
        str, typer.Option("--skill_id", help="ID of skill in WXO")
    ] = None,
    skill_operation_path: Annotated[
        str, typer.Option("--skill_operation_path", help="Skill operation path in WXO")
    ] = None,
):
    tools_controller.import_tool(
        kind=kind,
        file=file,
        skillset_id=skillset_id,
        skill_id=skill_id,
        skill_operation_path=skill_operation_path,
    )
