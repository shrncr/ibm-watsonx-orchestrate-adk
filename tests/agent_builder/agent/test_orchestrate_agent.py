import pytest

from pydantic_core import ValidationError

from ibm_watsonx_orchestrate.agent_builder.agents.orchestrate_agent import OrchestrateAgent
from ibm_watsonx_orchestrate.agent_builder.agents.types import SupervisorConfig

@pytest.fixture()
def orchestrate_agent_for_all_types():
    return {
        "name": "test_orchestrate_agent",
        "management_style": "supervisor",
        "management_style_config": {
            "reflection_enabled": True,
            "reflection_retry_count": 4
        },
        "llm": "test_llm",
        "agents": [
            "test_agent_1",
            "test_agent_2"
        ]
    }

@pytest.fixture(params=['name', 'management_style', 'management_style_config', 'goal' 'agents'])
def orchestrate_agent_missing_values(request, orchestrate_agent_for_all_types):
    orchestrate_spec_definition = orchestrate_agent_for_all_types
    orchestrate_spec_definition.pop(request.param, None)

    return {
        "missing" : request.param,
        "spec" : orchestrate_spec_definition
    }

@pytest.mark.asyncio
async def test_all_orchestrate_agent_types_with_spec(orchestrate_agent_for_all_types):
    orchestrate_spec_definition = orchestrate_agent_for_all_types

    orchestrate_agent = OrchestrateAgent(
        name = orchestrate_spec_definition["name"],
        management_style = orchestrate_spec_definition["management_style"],
        management_style_config = SupervisorConfig(
            reflection_enabled = orchestrate_spec_definition["management_style_config"]["reflection_enabled"],
            reflection_retry_count = orchestrate_spec_definition["management_style_config"]["reflection_retry_count"],
        ),
        llm = orchestrate_spec_definition["llm"],
        agents = orchestrate_spec_definition["agents"],
    )
    
    assert orchestrate_agent.name == orchestrate_spec_definition["name"]
    assert orchestrate_agent.management_style == orchestrate_spec_definition["management_style"]
    assert orchestrate_agent.management_style_config.reflection_enabled == orchestrate_spec_definition["management_style_config"]["reflection_enabled"]
    assert orchestrate_agent.management_style_config.reflection_retry_count == orchestrate_spec_definition["management_style_config"]["reflection_retry_count"]
    assert orchestrate_agent.llm == orchestrate_spec_definition["llm"]
    assert orchestrate_agent.agents == orchestrate_spec_definition["agents"]

@pytest.mark.asyncio
async def test_all_orchestrate_agent_types_no_spec(orchestrate_agent_for_all_types):
    orchestrate_spec_definition = orchestrate_agent_for_all_types

    orchestrate_agent = OrchestrateAgent(
        name = orchestrate_spec_definition["name"],
        management_style = orchestrate_spec_definition["management_style"],
        management_style_config = SupervisorConfig(
            reflection_enabled = orchestrate_spec_definition["management_style_config"]["reflection_enabled"],
            reflection_retry_count = orchestrate_spec_definition["management_style_config"]["reflection_retry_count"],
        ),
        llm = orchestrate_spec_definition["llm"],
        agents = orchestrate_spec_definition["agents"],
    )
    
    assert orchestrate_agent.name == orchestrate_spec_definition["name"]
    assert orchestrate_agent.management_style == orchestrate_spec_definition["management_style"]
    assert orchestrate_agent.management_style_config.reflection_enabled == orchestrate_spec_definition["management_style_config"]["reflection_enabled"]
    assert orchestrate_agent.management_style_config.reflection_retry_count == orchestrate_spec_definition["management_style_config"]["reflection_retry_count"]
    assert orchestrate_agent.llm == orchestrate_spec_definition["llm"]
    assert orchestrate_agent.agents == orchestrate_spec_definition["agents"]

@pytest.mark.asyncio
async def test_all_orchestrate_agent_spec_validation(orchestrate_agent_missing_values):
    agent_spec = orchestrate_agent_missing_values["spec"]
    missing_field = orchestrate_agent_missing_values["missing"]

    try:
        _ = OrchestrateAgent(
            name = agent_spec.get("name", None),
            management_style = agent_spec.get("management_style", None),
            management_style_config = SupervisorConfig(
                reflection_enabled = agent_spec.get("management_style_config", {}).get("reflection_enabled", None),
                reflection_retry_count = agent_spec.get("management_style_config", {}).get("reflection_retry_count", None),
            ),
            llm = agent_spec.get("llm", None),
            agents = agent_spec.get("agents", None),
        )
    except ValidationError as e:
        if f"Value error, {missing_field} is required" in str(e):
            assert True
        elif f"Input should be 'supervisor'" in str(e):
            assert True
        else:
            assert False
