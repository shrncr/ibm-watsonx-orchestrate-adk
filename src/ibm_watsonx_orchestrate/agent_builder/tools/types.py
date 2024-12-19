from enum import Enum
from typing import List, Any, Dict, Literal

from pydantic import BaseModel

class ToolPermission(str, Enum):
    READ_ONLY = 'READ_ONLY'
    WRITE_ONLY = 'WRITE_ONLY'
    READ_WRITE = 'READ_WRITE'
    ADMIN = 'ADMIN'


class JsonSchemaObject(BaseModel):
    type: Any = None
    title: str = None
    description: str = None
    properties: Dict[str, 'JsonSchemaObject'] = None
    required: List[str] = None
    items: 'JsonSchemaObject' = None
    uniqueItems: bool = None
    default: Any = None
    enum: List[Any] = None
    minimum: float = None
    maximum: float = None
    minLength: int = None
    maxLength: int = None
    format: str = None
    anyOf: List['JsonSchemaObject'] = None
    in_field: Literal['query', 'head', 'path', 'body'] = None


class ToolRequestBody(BaseModel):
    type: Literal['object']
    properties: Dict[str, JsonSchemaObject]
    required: List[str]
    anyOf: List['JsonSchemaObject'] = None


class ToolResponseBody(BaseModel):
    type: Literal['object', 'string', 'number', 'integer', 'boolean', 'array','null'] = None
    description: str = None
    properties: Dict[str, JsonSchemaObject] = None
    items: JsonSchemaObject = None
    uniqueItems: bool = None
    anyOf: List['JsonSchemaObject'] = None
    required: List[str] = None


class OpenApiSecurityScheme(BaseModel):
    type: Literal['apiKey', 'http', 'oauth2', 'openIdConnect']
    scheme: Literal['basic', 'bearer', 'oauth'] = None
    in_field: Literal['query', 'header', 'cookie'] = None
    name: str = None
    open_id_connect_url: str = None
    flows: dict = None


HTTP_METHOD = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


class OpenApiToolBinding(BaseModel):
    http_method: HTTP_METHOD
    http_path: str
    success_status_code: int = 200  # this is a diff from the spec
    security: List[OpenApiSecurityScheme]
    servers: List[str]


class PythonToolBinding(BaseModel):
    function: str


class WxFlowsToolBinding(BaseModel):
    endpoint: str
    flow_name: str
    security: OpenApiSecurityScheme


class SkillToolBinding(BaseModel):
    skillset_id: str
    skill_id: str
    skill_operator_path: str
    http_method: HTTP_METHOD


class ClientSideToolBinding(BaseModel):
    pass


class ToolBinding(BaseModel):
    openapi: OpenApiToolBinding = None
    python: PythonToolBinding = None
    wxflows: WxFlowsToolBinding = None
    skill: SkillToolBinding = None
    client_side: ClientSideToolBinding = None


class ToolSpec(BaseModel):
    name: str = None
    description: str = None
    permission: ToolPermission = None
    input_schema: ToolRequestBody = None
    output_schema: ToolResponseBody = None
    binding: ToolBinding = None


class OpenAPIRuntimeToolSecurityBinding(BaseModel):
    name: str
    username: str = None
    password: str = None
    api_key: str = None


class OpenAPIRuntimeServerBinding(BaseModel):
    server: str
    security_schema: OpenAPIRuntimeToolSecurityBinding = None

