import asyncio
from typing import Optional

import httpx
from pydantic import BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission, create_openapi_json_tool_from_uri


class CatFact(BaseModel):
    fact: str
    length: int

@tool(permission=ToolPermission.READ_WRITE)
async def get_cat_fact(max_length: Optional[int] = None) -> CatFact:
    """
    Get a collection of facts about cats
    :param max_length: the max length of the string that is the cat fact
    :return: the list of facts about cats
    """
    query_string = f"?max_length={max_length}" if max_length is not None else ''
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://catfact.ninja/fact{query_string}")
        if r.status_code != 200:
            return None
        return CatFact.model_validate(r.json())


async def main():
    github_issues = await create_openapi_json_tool_from_uri(
        name='cat_facts', # the endpoint name and description would be used here, but was poor
        description='Fetch random facts about cats',

        openapi_uri='https://api.apis.guru/v2/specs/github.com/api.github.com/1.1.4/openapi.yaml',
        http_path='/issues',
        http_method='GET',
        http_success_response_code=200
    )

    github_issues.dump_spec('github_issues.yaml')
    github_issues.dump_spec('github_issues.json')

    get_cat_fact.dump_spec('get_cat_fact_python.yaml')


if __name__ == '__main__':
    asyncio.run(main())
