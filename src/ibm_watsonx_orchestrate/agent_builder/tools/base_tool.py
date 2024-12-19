import json

import yaml

from .types import ToolSpec


class BaseTool:
    spec: ToolSpec

    def __init__(self, spec: ToolSpec):
        self.spec = spec


    def __call__(self, **kwargs):
        pass

    def dump_spec(self, file: str) -> None:
        dumped = self.spec.model_dump(mode='json', exclude_unset=True)
        with open(file, 'w') as f:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml.dump(dumped, f)
            elif file.endswith('.json'):
                json.dump(dumped, f, indent=2)
            else:
                raise ValueError('file must end in .json, .yaml, or .yml')

    def dumps_spec(self) -> str:
        dumped = self.spec.model_dump(mode='json', exclude_unset=True)
        return json.dumps(dumped, indent=2)

    def __repr__(self):
        return f"Tool(name='{self.spec.name}', description='{self.spec.description}')"
