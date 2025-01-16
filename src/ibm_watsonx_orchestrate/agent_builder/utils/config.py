from typing import Literal
import os

from pydantic import BaseModel


class RuntimeContext(BaseModel):
    environment: Literal['local', 'orchestrate'] = 'local'


runtime_context = RuntimeContext(
    environment=os.getenv('RUNTIME_ENVIRONMENT') or 'local'
)
