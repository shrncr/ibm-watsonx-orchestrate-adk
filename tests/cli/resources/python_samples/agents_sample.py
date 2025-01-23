# research_agent.py
from pydantic import BaseModel, Field
import asyncio

from ibm_watsonx_orchestrate.agent_builder.agents import ExpertAgent, OrchestrateAgent, SupervisorConfig
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission, create_openapi_json_tool_from_uri


class Message(BaseModel):
    prefix: str = Field(desc='What to say before the message text')
    message: str = Field(desc='The message that was sent')


@tool(name="echo", description="the description", permission=ToolPermission.READ_ONLY)
def echo(input: Message) -> str:
    """
    A sample tool which just repeats what you said
    :param input: The message that was sent to this echo bot, including the prefix
    """
    return f'{input.prefix} {input.message}'


get_github_issues = asyncio.run(create_openapi_json_tool_from_uri(
    name='get_github_issues',
    description='Get issues from github',
    openapi_uri='https://api.apis.guru/v2/specs/github.com/api.github.com/1.1.4/openapi.yaml',
    http_path='/issues',
    http_method='GET',
    http_success_response_code=200
))

research_agent_1 = ExpertAgent(
    name="research_agent",
    type="expert",
    description="A Research Assistant which can query the web to help the user with research tasks that require current knowledge or open data from the web to complete.",
    role="You are a helpful and ethical AI research assistant that uses web search tools to answer user questions.",
    goal="Answer the user's question using the information found on the web.",
    instructions="Use the tools provided to answer the user's question.  If you do not have enough information to answer the question, say so.  If you need more information, ask follow up questions.",
    tools=['echo'],
)

research_agent_2 = ExpertAgent(
    name="github_agent",
    type="expert",
    description="A Research Assistant which can query the web to help the user with research tasks that require current knowledge or open data from the web to complete.",
    role="You are a helpful and ethical AI research assistant that uses web search tools to answer user questions.",
    goal="Answer the user's question using the information found on the web.",
    instructions="Use the tools provided to answer the user's question.  If you do not have enough information to answer the question, say so.  If you need more information, ask follow up questions.",
    tools=['get_github_issues']
)

orchestrator_agent = OrchestrateAgent(
    name="sample_orchestrator_agent",
    type="orchestrator",
    management_style="supervisor",
    management_style_config=SupervisorConfig(reflection_enabled=True, reflection_retry_count=3),
    llm="granite",
    # note working out bug, it should be possible to reference by string or by instance
    agents=[research_agent_1, "research_agent_2"],
)


# Sample commands
# orchestrate login
# orchestrate tools import -k openapi -f /Users/emarcoux/Workspaces/assistant/wxo-clients/tests/agent_builder/fixtures/testitall.openapi.json
# orchestrate tools import -k python -f /Users/emarcoux/Workspaces/assistant/wxo-clients/examples/agent_builder/demo/demo.py

# orchestrate agents import -f examples/agent_builder/demo/demo.py

# orchestrate agents create \
#    --name sample_expert_agent \
#    --type expert \
#    --description "Sample agent description" \
#    --role "You are a sample agent meant to demonstrate the syntax" \
#    --goal "Your mission is to teach people the syntax of the WXO CLI" \
#    --instructions "Use the tools provided to ..." \
#    --tools web_search,my_tool


# orchestrate agents create \
#    --name sample_orchestrator_agent \
#    --type orchestrator \
#    --management_style supervisor \
#    --management_style_config reflection_enabled=true,reflection_retry_count=3 \
#    --llm granite \
#    --agents sample_expert_agent,sales_agent

# orchestrate connections application create --app-id my_app_id -t basic -u username -p password
# orchestrate tools import -k openapi -f /Users/emarcoux/Workspaces/assistant/wxo-clients/tests/agent_builder/fixtures/testitall.openapi.json --app-id=my_app_id