import asyncio

from ibm_watsonx_orchestrate.agent_builder.tools import PythonTool,  OpenAPIRuntimeServerBinding
from ibm_watsonx_orchestrate.agent_builder.tools.integrations.langchain import as_langchain_tool


async def main():
    get_cat_fact = PythonTool.from_spec('get_cat_fact_python.yaml')
    # openapi_cat_facts_tool = OpenAPITool.from_spec(
    #     file='openapi_cat_facts.yaml',
    #     runtime_server_binding=OpenAPIRuntimeServerBinding(
    #         server='https://catfact.ninja'
    #     )
    # )

    langgraph_get_facts_tool = get_cat_fact.to_langchain_tool()
    # langgraph_openapi_cat_facts_tool = openapi_cat_facts_tool.to_langchain_tool()

    print(await langgraph_get_facts_tool.ainvoke(input={'max_length': 40}))
    # print('---')
    # print(await langgraph_openapi_cat_facts_tool.ainvoke(input={'max_length': 40}))

if __name__ == '__main__':
    asyncio.run(main())
