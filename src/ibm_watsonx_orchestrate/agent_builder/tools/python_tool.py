import importlib
import inspect
import json
import os
from types import NoneType

import docstring_parser
import yaml
from pydantic import TypeAdapter
import jsonref

from .types import ToolSpec, ToolPermission, ToolRequestBody, ToolResponseBody, JsonSchemaObject, ToolBinding, \
    PythonToolBinding
from .base_tool import BaseTool
from ..utils.config import runtime_context

_all_tools = []


class PythonTool(BaseTool):
    def __init__(self, fn, spec: ToolSpec):
        BaseTool.__init__(self, spec=spec)
        self.fn = fn

    def __call__(self, *args, **kwargs):
        if runtime_context.environment == 'local':
            return self.fn(*args, **kwargs)
        else:
            # Invoke the function on the runtime
            # Includes binding information about what module nad method to call
            pass

    @staticmethod
    def from_spec(file: str) -> 'PythonTool':
        with open(file, 'r') as f:
            if file.endswith('.yaml') or file.endswith('.yml'):
                spec = ToolSpec.model_validate(yaml.safe_load(f))
            elif file.endswith('.json'):
                spec = ToolSpec.model_validate(json.load(f))
            else:
                raise ValueError('file must end in .json, .yaml, or .yml')

        if spec.binding.python is None or spec.binding.python is None:
            raise ValueError('failed to load python tool as the tool had no python binding')

        [module, fn_name] = spec.binding.python.function.split(':')
        fn = getattr(importlib.import_module(module), fn_name)

        return PythonTool(fn=fn, spec=spec)

    def __repr__(self):
        return f"PythonTool(fn={self.spec.binding.python.function}, name='{self.spec.name}', description='{self.spec.description}')"

    def __str__(self):
        return self.__repr__()


def tool(
    name: str = None,
    description: str = None,
    input_schema: ToolRequestBody = None,
    output_schema: ToolResponseBody = None,
    permission: ToolPermission = ToolPermission.READ_ONLY
) -> PythonTool:
    """
    Decorator to convert a python function into a callable tool.

    Support level: Beta

    :param name: the agent facing name of the tool (defaults to the function name)
    :param description: the description of the tool (used for tool routing by the agent)
    :param input_schema: the json schema args to the tool
    :param output_schema: the response json schema for the tool
    :param permission: the permissions needed by the user of the agent to invoke the tool
    :return:
    """
    # inspiration: https://github.com/pydantic/pydantic/blob/main/pydantic/validate_call_decorator.py
    def _tool_decorator(fn):
        spec = ToolSpec()
        spec.name = name or fn.__name__
        spec.description = description
        spec.permission = permission

        t = PythonTool(fn=fn, spec=spec)
        spec.binding = ToolBinding(python=PythonToolBinding(function=''))

        if fn.__doc__ is not None:
            doc = docstring_parser.parse(fn.__doc__)
        else:
            doc = None

        if spec.description is None and doc is not None:
            spec.description = doc.description

        function_binding = (inspect.getsourcefile(fn)
                            .replace(os.getcwd()+'/', '')
                            .replace('.py', '')
                            .replace('/','.') +
                            f":{fn.__name__}")
        spec.binding.python.function = function_binding

        sig = inspect.signature(fn)
        if not input_schema:
            spec.input_schema = ToolRequestBody(
                type='object',
                properties={},
                required=[]
            )

            params = sig.parameters
            for n, param in params.items():
                is_optional = param.annotation is None or param.annotation.__name__ == 'Optional'
                if param.default is param.empty and not is_optional:
                    spec.input_schema.required.append(n)

                if param.annotation:
                    annotation = next(filter(lambda x: not isinstance(x, NoneType), param.annotation.__args__), None) \
                        if param.annotation.__name__ == 'Optional' \
                        else param.annotation

                    spec.input_schema.properties[n] = JsonSchemaObject.parse_obj(jsonref.replace_refs(TypeAdapter(annotation).json_schema()))
                else:
                    spec.input_schema.properties[n] = JsonSchemaObject(properties={}) if param.annotation is not None else JsonSchemaObject(type='null')

                doc_arg = next(filter(lambda x: x.arg_name == n, doc.params if doc is not None else []), None)
                if doc_arg:
                    spec.input_schema.properties[n].description = doc_arg.description

        else:
            spec.input_schema = input_schema

        if not output_schema:
            ret = sig.return_annotation
            if ret != sig.empty:
                spec.output_schema = ToolResponseBody.parse_obj(jsonref.replace_refs(TypeAdapter(ret).json_schema()))
            else:
                spec.output_schema = ToolResponseBody(properties={})

            if doc is not None and doc.returns is not None and doc.returns.description is not None:
                spec.output_schema.description = doc.returns.description

        else:
            spec.output_schema = ToolResponseBody()
        _all_tools.append(t)
        return t

    return _tool_decorator


def get_all_python_tools():
    return [t for t in _all_tools]
