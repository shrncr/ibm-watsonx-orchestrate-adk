import asyncio
from typing import Optional

import httpx
from pydantic import BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class CatFact(BaseModel):
    fact: str
    length: int

@tool(permission=ToolPermission.READ_WRITE)
async def get_cat_fact(max_length: Optional[int]) -> CatFact:
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
    # openapi_cat_facts_tool = await create_openapi_json_tool_from_uri(
    #     name='cat_facts', # the endpoint name and description would be used here, but was poor
    #     description='Fetch random facts about cats',
    #
    #     openapi_uri='https://catfact.ninja/docs/api-docs.json',
    #     http_path='/facts',
    #     http_method='GET',
    #     http_success_response_code=200,  # this defaults to 200
    #
    #     # The actual return value for this open api spec doesn't match its schema
    #     # so we're overriding it here
    #     output_schema=ToolResponseBody(
    #         type='object',
    #         properties={
    #             'data': JsonSchemaObject(
    #                 type='object',
    #                 properties={
    #                     'fact': JsonSchemaObject(type='string'),
    #                     'length': JsonSchemaObject(type='integer')
    #                 }
    #             )
    #         }
    #     ),
    #
    #     # note this is lazily bound (not part of the spec)
    #     # in case the user has dev/stg/prd apis, not really needed for gen
    #     runtime_server_binding=OpenAPIRuntimeServerBinding(
    #         server='https://catfact.ninja'
    #     )
    # )

    # openapi_cat_facts_tool.dump_spec('openapi_cat_facts.yaml')
    # openapi_cat_facts_tool.dump_spec('openapi_cat_facts.json')

    get_cat_fact.dump_spec('get_cat_fact_python.yaml')


if __name__ == '__main__':
    asyncio.run(main())
