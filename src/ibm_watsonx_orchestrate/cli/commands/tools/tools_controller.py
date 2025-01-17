import typer
from typing import Generator
from enum import Enum
import importlib
import json
import sys
from pathlib import Path
import rich
import inspect

class ToolKind(str, Enum):
    openapi = "openapi"
    python = "python"
    skill = "skill"


def validate_params(kind: ToolKind, **args) -> None:
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

    decorated_funtions = list(functionsWithDecorator(module, "tool"))

    for function in decorated_funtions:
        spec = json.loads(getattr(module, function).dumps_spec())
        rich.print_json(data=spec)


# def import_openapi_tool(file: str) -> None:
    # with open(file, "r") as f:
    #     yaml_content = yaml.load(f, Loader=yaml.SafeLoader)

    # # TODO: account to multiple http verbs, multiple paths
    # endpoint_path = list(yaml_content["paths"].keys())[0]
    # http_method = list(yaml_content["paths"][endpoint_path].keys())[0]

    # cfg = Config()
    # api_key = cfg.read(AUTH_SECTION_HEADER, AUTH_MCSP_API_KEY_OPT)

    # tool = create_openapi_json_tool(
    #     yaml_content,
    #     http_path=endpoint_path,
    #     http_method=http_method.upper(),
    #     runtime_server_binding=OpenAPIRuntimeServerBinding(
    #         server="http://localhost:3000",
    #         credentials=OpenAPIRuntimeAPIBasicCredentials(key="auth", api_key=api_key),
    #     ),
    # )

    # spec = json.loads(tool.dumps_spec())
    # rich.print_json(data=spec)


def import_tool(kind: ToolKind, **args) -> None:
    validate_params(kind=kind, **args)

    match kind:
        case "python":
            import_python_tool(file=args["file"])
        case "openapi":
            # import_openapi_tool(file=args["file"])
            print("OpenAPI Import not implemented yet")
        case "skill":
            print("Skill Import not implemented yet")
        case _:
            raise ValueError("Invalid kind selected")
