# research_agent.py
from ibm_watsonx_orchestrate.agent_builder.agents import ExpertAgent, OrchestrateAgent, SupervisorConfig
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="myName", description="the description", permission=ToolPermission.ADMIN)
def my_tool(input: str) -> str:
    pass

research_agent_1 = ExpertAgent(
    name="research_agent",
    type="expert",
    description="A Research Assistant which can query the web to help the user with research tasks that require current knowledge or open data from the web to complete.",
    role="You are a helpful and ethical AI research assistant that uses web search tools to answer user questions.",
    goal="Answer the user's question using the information found on the web.",
    instructions="Use the tools provided to answer the user's question.  If you do not have enough information to answer the question, say so.  If you need more information, ask follow up questions.",
    tools=[my_tool],
)

orchestrator_agent = OrchestrateAgent(
      name="sample_orchestrator_agent",
      type="orchestrator",
      management_style="supervisor",
      management_style_config=SupervisorConfig(reflection_enabled=True, reflection_retry_count=3),
      llm="granite",
      agents=["research_agent"],
   )