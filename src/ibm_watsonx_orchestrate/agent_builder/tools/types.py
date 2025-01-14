from enum import Enum
from typing import List, Any, Dict, Literal, Optional

from pydantic import BaseModel, model_validator, ConfigDict, Field


class ToolPermission(str, Enum):
    READ_ONLY = 'READ_ONLY'
    WRITE_ONLY = 'WRITE_ONLY'
    READ_WRITE = 'READ_WRITE'
    ADMIN = 'ADMIN'


class JsonSchemaObject(BaseModel):
    model_config = ConfigDict(extra='allow')

    type: Literal['object', 'string', 'number', 'integer', 'boolean', 'array', 'null'] = 'object'
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
    in_field: Optional[Literal['query', 'header', 'path', 'body']] = Field(None, alias='in')


class ToolRequestBody(BaseModel):
    model_config = ConfigDict(extra='allow')

    type: Literal['object']
    properties: Dict[str, JsonSchemaObject]
    required: List[str]


class ToolResponseBody(BaseModel):
    model_config = ConfigDict(extra='allow')

    type: Literal['object', 'string', 'number', 'integer', 'boolean', 'array','null'] = None
    description: str = None
    properties: Dict[str, JsonSchemaObject] = None
    items: JsonSchemaObject = None
    uniqueItems: bool = None
    anyOf: List['JsonSchemaObject'] = None
    required: List[str] = None


class OpenApiSecurityScheme(BaseModel):
    model_config = ConfigDict(extra='allow')

    type: Literal['apiKey', 'http', 'oauth2', 'openIdConnect']
    scheme: Literal['basic', 'bearer', 'oauth'] = None
    in_field: Literal['query', 'header', 'cookie'] = None
    name: str = None
    open_id_connect_url: str = None
    flows: dict = None

    @model_validator(mode='after')
    def validate_security_scheme(self) -> 'OpenApiSecurityScheme':
        if self.type == 'http' and self.scheme is None:
            raise ValueError("'scheme' is required when type is 'http'")

        if self.type == 'oauth2' and self.flows is None:
            raise ValueError("'flows' is required when type is 'oauth2'")

        if self.type == 'openIdConnect' and self.open_id_connect_url is None:
            raise ValueError("'open_id_connect_url' is required when type is 'openIdConnect'")

        if self.type == 'apiKey':
            if self.name is None:
                raise ValueError("'name' is required when type is 'apiKey'")
            if self.in_field is None:
                raise ValueError("'in_field' is required when type is 'apiKey'")

        return self


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

    @model_validator(mode='after')
    def validate_security_scheme(self) -> 'WxFlowsToolBinding':
        if self.security.type != 'apiKey':
            raise ValueError("'security' scheme must be of type 'apiKey'")
        return self


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

    @model_validator(mode='after')
    def validate_binding_type(self) -> 'ToolBinding':
        bindings = [
            self.openapi is not None,
            self.python is not None,
            self.wxflows is not None,
            self.skill is not None,
            self.client_side is not None
        ]
        if sum(bindings) == 0:
            raise ValueError("One binding must be set")
        if sum(bindings) > 1:
            raise ValueError("Only one binding can be set")
        return self


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

