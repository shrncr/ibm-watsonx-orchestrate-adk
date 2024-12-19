import json
from typing import Callable

import yaml
import pathlib
import httpx
import jsonref
from .types import ToolSpec
from .base_tool import BaseTool
from .types import HTTP_METHOD, ToolPermission, ToolRequestBody, ToolResponseBody, \
    OpenApiToolBinding, \
    OpenAPIRuntimeServerBinding, JsonSchemaObject, ToolBinding, OpenApiSecurityScheme
from ..utils.config import runtime_context


def _resolve_value(name, values, schema):
    value = values.get(name)
    if value is None:
        value = schema.default
    return value


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")

    def __str__(self):
        return f"{self.status_code} {self.message}"


class OpenAPITool(BaseTool):
    runtime_server_binding: OpenAPIRuntimeServerBinding

    def __init__(self, spec: ToolSpec, runtime_server_binding: OpenAPIRuntimeServerBinding = None):
        BaseTool.__init__(self, spec=spec)
        self.runtime_server_binding = runtime_server_binding

    async def __call__(self, **kwargs):
        schema = self.spec.input_schema
        if self.runtime_server_binding is None:
            raise ValueError('runtime_server_binding was not configured')

        url = self.runtime_server_binding.server + self.spec.binding.openapi.http_path
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        query_params = {}
        request_body = {}

        for n, param in schema.properties.items():
            value = _resolve_value(n, kwargs, param)
            if value is None:
                if n in schema.required:
                    raise ValueError(f"Missing required parameter: {n}")
                else:
                    continue

            if param.in_field == 'head':
                headers[n] = value
            elif param.in_field == 'path':
                url = url.replace('{'+n+'}', value)
            elif param.in_field == 'query':
                query_params[n] = value
            elif param.in_field == 'body':
                request_body[n] = value
            else:
                raise ValueError(f"Invalid in_field {n}: {param.in_field}, {param}")

        if runtime_context.environment == 'local':
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    self.spec.binding.openapi.http_method,
                    httpx.URL(url),
                    headers=headers,
                    params=query_params,
                    json=request_body if len(request_body.keys()) > 0 else None
                )
                if resp.status_code != self.spec.binding.openapi.success_status_code:
                    raise HTTPException(resp.status_code, f" failed with status code: {resp.status_code}\n{resp.text}")
                return resp.json()
        else:
            # invoke incoming webhooks so there so the request comes from a set of dedicated pool of
            # ip addresses the customer can whitelist
            pass

    @staticmethod
    def from_spec(file: str, runtime_server_binding: OpenAPIRuntimeServerBinding) -> 'OpenAPITool':
        with open(file, 'r') as f:
            if file.endswith('.yaml') or file.endswith('.yml'):
                spec = ToolSpec.model_validate(yaml.safe_load(f))
            elif file.endswith('.json'):
                spec = ToolSpec.model_validate(json.load(f))
            else:
                raise ValueError('file must end in .json, .yaml, or .yml')

        if spec.binding.openapi is None or spec.binding.openapi is None:
            raise ValueError('failed to load python tool as the tool had no openapi binding')

        return OpenAPITool(spec=spec, runtime_server_binding=runtime_server_binding)

    def __repr__(self):
        return f"OpenAPITool(fn={self.spec.binding.python.function}, name='{self.spec.name}', description='{self.spec.description}')"

    def __str__(self):
        return self.__repr__()


def create_openapi_json_tool(
        openapi_spec: dict,
        http_path: str,
        http_method: HTTP_METHOD,
        http_success_response_code: int = 200,
        http_response_content_type='application/json',
        name: str = None,
        description: str = None,
        permission: ToolPermission = ToolPermission.READ_ONLY,
        input_schema: ToolRequestBody = None,
        output_schema: ToolResponseBody = None,
        runtime_server_binding: OpenAPIRuntimeServerBinding = None
) -> OpenAPITool:
    """
    Creates a tool from an openapi spec

    Support level: Alpha

    :param openapi_spec: The parsed dictionary representation of an openapi spec
    :param http_path: Which path to create a tool for
    :param http_method: Which method on that path to create the tool for
    :param http_success_response_code: Which http status code should be considered a successful call (defaults to 200)
    :param http_response_content_type: Which http response type should be considered successful (default to application/json)
    :param name: The name of the resulting tool (used to invoke the tool by the agent)
    :param description: The description of the resulting tool (used as the semantic layer to help the agent with tool selection)
    :param permission: Which orchestrate permission level does a user need to have to invoke this tool
    :param input_schema: The JSONSchema of the inputs to the http request
    :param output_schema: The expected JSON schema of the outputs of the http response
    :param runtime_server_binding: The runtime credentials to use with this tool
    :return: An OpenAPITool that can be used by an expert agent
    """
    spec = ToolSpec()
    spec.permission = permission
    spec.input_schema = input_schema or ToolRequestBody(
        type='object',
        properties={},
        required=[]
    )
    spec.output_schema = output_schema or ToolResponseBody(properties={}, required=[])

    # limitation does not support circular $refs
    openapi_contents = jsonref.replace_refs(openapi_spec)


    paths = openapi_contents.get('paths', {})
    route = paths.get(http_path)
    if route is None:
        raise ValueError(f"Path {http_path} not found in paths. Available endpoints are: {list(paths.keys())}")

    route_spec = route.get(http_method.lower(), route.get(http_method.upper()))
    if route_spec is None:
        raise ValueError(f"Path {http_path} did not have an http_method {http_method}. Available methods are {list(route.keys())}")

    spec.name = name or route_spec.get('operationId', None)
    if spec.name is None:
        raise ValueError(f"No name provided for tool. {http_method}: {http_path} did not an operationId, and no name was provided")

    spec.description = description or route_spec.get('description')
    parameters = route_spec['parameters']
    for parameter in parameters:
        name = parameter['name']
        if parameter['required']:
            spec.input_schema.required.append(name)
        parameter['schema']['title'] = parameter['name']
        parameter['schema']['description'] = parameter['description']
        spec.input_schema.properties[name] = JsonSchemaObject.model_validate(parameter['schema'])
        spec.input_schema.properties[name].in_field = parameter['in']

    responses = route_spec.get('responses', {})
    response = responses.get(str(http_success_response_code), {})
    response_description = response.get('description')
    response_schema = response.get('content', {}).get(http_response_content_type, {}).get('schema', {})

    response_schema['required'] = []
    spec.output_schema = ToolResponseBody.model_validate(response_schema)
    spec.output_schema.description = response_description

    servers = list(map(lambda x: x if isinstance(x, str) else x['url'], openapi_contents.get('servers', openapi_contents.get('x-servers', []))))

    rawOpenAPIsecuritySchemes = openapi_contents.get('components', {}).get('securitySchemes', {})
    securitySchemesMap = {}
    for name, securityScheme in rawOpenAPIsecuritySchemes.items():
        securitySchemesMap[name] = OpenApiSecurityScheme(
            type=securityScheme.get('type'),
            scheme=securityScheme.get('scheme'),
            flows=securityScheme.get('flows'),
            name=name,
            open_id_connect_url=securityScheme.get('openId', {}).get('openIdConnectUrl')
        )

    # note we have no concept of scope because to a user their auth cred either has access or it doesn't
    # unless we ask them for a scope they don't know to validate it provides no value
    security = []
    for needed_security in route_spec.get('security', []):
        name = next(needed_security.keys(), None)
        if name is None or name not in securitySchemesMap:
            raise ValueError(f"Invalid openapi spec, {HTTP_METHOD} {http_path} asks for a security scheme of {name}, "
                             f"but no such security scheme was configured in the .security section of the spec")

        security.append(securitySchemesMap[name])

    spec.binding = ToolBinding(openapi=OpenApiToolBinding(
        http_path=http_path,
        http_method=http_method,
        security=security,
        servers=servers
    ))

    return OpenAPITool(spec=spec, runtime_server_binding=runtime_server_binding)


async def create_openapi_json_tool_from_uri(
        openapi_uri: str,
        http_path: str,
        http_method: HTTP_METHOD,
        http_success_response_code: int = 200,
        http_response_content_type='application/json',
        permission: ToolPermission = ToolPermission.READ_ONLY,
        name: str = None,
        description: str = None,
        input_schema: ToolRequestBody = None,
        output_schema: ToolResponseBody = None,
        runtime_server_binding: OpenAPIRuntimeServerBinding = None
) -> OpenAPITool:
    """
    Creates a tool from an openapi spec

    :param openapi_uri: The uri to the openapi spec to generate the tool from (ie file://path/to/openapi_file.json, https://catfact.ninja/docs/api-docs.json)
    :param http_path: Which path to create a tool for
    :param http_method: Which method on that path to create the tool for
    :param http_success_response_code: Which http status code should be considered a successful call (defaults to 200)
    :param http_response_content_type: Which http response type should be considered successful (default to application/json)
    :param name: The name of the resulting tool (used to invoke the tool by the agent)
    :param description: The description of the resulting tool (used as the semantic layer to help the agent with tool selection)
    :param permission: Which orchestrate permission level does a user need to have to invoke this tool
    :param input_schema: The JSONSchema of the inputs to the http request
    :param output_schema: The expected JSON schema of the outputs of the http response
    :param runtime_server_binding:
    :return: An OpenAPITool that can be used by an expert agent
    """
    if openapi_uri.startswith('file://'):
        path = str(pathlib.Path(openapi_uri.replace('file:/', '')).resolve())
        with open(path, 'r') as fp:
            if path.endswith('.json'):
                openapi_contents = json.load(fp)
            elif path.endswith('.yaml') or path.endswith('.yml'):
                openapi_contents = yaml.load(fp)
            else:
                raise ValueError(f"Unexpected file extension for file {path}, expected one of [.json, .yaml, .yml]")
    elif openapi_uri.endswith('.json'):
        async with httpx.AsyncClient() as client:
            r = await client.get(openapi_uri)
            if r.status_code != 200:
                raise ValueError(f"Failed to fetch an openapi spec from {openapi_uri}, status code: {r.status_code}")
            openapi_contents = r.json()

    if openapi_contents is None:
        raise ValueError(f"Unrecognized openapi_uri pattern {openapi_uri}")

    return create_openapi_json_tool(
        openapi_spec=openapi_contents,
        http_path=http_path,
        http_method=http_method,
        http_success_response_code=http_success_response_code,
        http_response_content_type=http_response_content_type,
        permission=permission,
        name=name,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        runtime_server_binding=runtime_server_binding
    )
