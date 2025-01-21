import asyncio

import typer
from typing import Generator
from enum import Enum
import importlib
import json
import sys
from pathlib import Path
import rich
import inspect

from ibm_watsonx_orchestrate.agent_builder.tools import create_openapi_json_tools_from_uri



class ToolKind(str, Enum):
    openapi = "openapi"
    python = "python"
    skill = "skill"


def validate_params(kind: ToolKind, **args) -> None:
    if kind != 'openapi' and args.get('app_id') is not None:
        raise typer.BadParameter(
            "--app_id parameter can only be used with openapi tools"
        )

    if kind in {"openapi", "python"} and args["file"] is None:
        raise typer.BadParameter(
            "--file (-f) is required when kind is set to either python or openapi"
        )
    elif kind == "skill":
        missing_params = []
        if args["skillset_id"] is None:
            missing_params.append("--skillset_id")
        if args["skill_id"] is None:
            missing_params.append("--skill_id")
        if args["skill_operation_path"] is None:
            missing_params.append("--skill_operation_path")

        if len(missing_params) > 0:
            raise typer.BadParameter(
                f"Missing flags {missing_params} required for kind skill"
            )


def functionsWithDecorator(
    module: any, decorator_name: str
) -> Generator[str, None, None]:
    sourcelines = inspect.getsourcelines(module)[0]
    for i, line in enumerate(sourcelines):
        line = line.strip()
        if line.split("(")[0].strip() == "@" + decorator_name:
            nextLine = sourcelines[i + 1]
            name = nextLine.split("def")[1].split("(")[0].strip()
            yield (name)


def import_python_tool(file: str) -> None:
    file_path = Path(file)
    file_directory = file_path.parent
    file_name = file_path.stem
    sys.path.append(str(file_directory))
    module = importlib.import_module(file_name)

    decorated_functions = list(functionsWithDecorator(module, "tool"))

    for function in decorated_functions:
        spec = json.loads(getattr(module, function).dumps_spec())
        rich.print_json(data=spec)


async def import_openapi_tool(file: str, app_id: str) -> None:
    tools = await create_openapi_json_tools_from_uri(file, app_id)

    rich.print_json(data=[tool.__tool_spec__.model_dump(exclude_none=True, exclude_unset=True, by_alias=True) for tool in tools])



def import_tool(kind: ToolKind, **args) -> None:
    validate_params(kind=kind, **args)

    match kind:
        case "python":
            import_python_tool(file=args["file"])
        case "openapi":
            asyncio.run(import_openapi_tool(file=args["file"], app_id=args.get('app_id')))
        case "skill":
            print("Skill Import not implemented yet")
        case _:
            raise ValueError("Invalid kind selected")
