from langchain_core.tools import StructuredTool

from ..base_tool import BaseTool as OrchestrateBaseTool

def as_langchain_tool(tool: OrchestrateBaseTool) -> StructuredTool:
    from ...utils.pydantic_utils import generate_schema_only_base_model

    tool = StructuredTool.from_function(
        name=tool.__tool_spec__.name,
        description=tool.__tool_spec__.description,
        args_schema=generate_schema_only_base_model(tool.__tool_spec__.input_schema),
        infer_schema=False,
        parse_docstring=False,
        coroutine=tool
    )
    return tool
