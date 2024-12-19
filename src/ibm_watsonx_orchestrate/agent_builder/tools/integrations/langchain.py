from langchain_core.tools import StructuredTool

from ..base_tool import BaseTool as OrchestrateBaseTool
from ...utils.pydantic_utils import generate_schema_only_base_model

def as_langchain_tool(tool: OrchestrateBaseTool) -> StructuredTool:
    tool = StructuredTool.from_function(
        name=tool.spec.name,
        description=tool.spec.description,
        args_schema=generate_schema_only_base_model(tool.spec.input_schema),
        infer_schema=False,
        parse_docstring=False,
        coroutine=tool
    )
    return tool
