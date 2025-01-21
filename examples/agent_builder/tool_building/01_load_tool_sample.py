import asyncio

from ibm_watsonx_orchestrate.agent_builder.tools import PythonTool, OpenAPITool


async def main():
    get_cat_fact = PythonTool.from_spec('get_cat_fact_python.yaml')
    github_issues = OpenAPITool.from_spec(
        file='github_issues.yaml',
    )

    langgraph_get_facts_tool = get_cat_fact.to_langchain_tool()
    langgraph_github_issues = github_issues.to_langchain_tool()

    print(await langgraph_get_facts_tool.ainvoke(input={'max_length': 40}))
    print('---')
    print(await langgraph_github_issues.ainvoke(input={}))

if __name__ == '__main__':
    asyncio.run(main())
