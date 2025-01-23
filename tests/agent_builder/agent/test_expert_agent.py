import pytest

from pydantic_core import ValidationError

from ibm_watsonx_orchestrate.agent_builder.agents.expert_agent import ExpertAgent

@pytest.fixture(params=['expert'])
def expert_agent_for_all_types(request):
    return request.param, {
        "name": f"test_{request.param}_name",
        "description": f"Test Object for expert agent with type: {request.param}",
        "type": request.param,
        "role": "Test Role",
        "goal": "Test Goal",
        "instructions": "Test Instruction",
        "tools": [
            "test_tool_1",
            "test_tool_2"
        ] if request.param == 'expert' else None
    }

@pytest.fixture(params=['name', 'type', 'role', 'goal', 'instructions', 'tools'])
def expert_agent_missing_values(request, expert_agent_for_all_types):
    agent_type, expert_spec_definition = expert_agent_for_all_types
    expert_spec_definition.pop(request.param, None)

    return {
        "type" : agent_type,
        "missing" : request.param,
        "spec" : expert_spec_definition
    }

@pytest.mark.asyncio
async def test_all_expert_agent_types_with_spec(expert_agent_for_all_types):
    _, expert_spec_definition = expert_agent_for_all_types

    expert_agent = ExpertAgent(
        name = expert_spec_definition["name"],
        description = expert_spec_definition["description"],
        type = expert_spec_definition["type"],
        role = expert_spec_definition["role"],
        goal = expert_spec_definition["goal"],
        instructions = expert_spec_definition["instructions"],
        tools = expert_spec_definition["tools"]
        )
    
    assert expert_agent.name == expert_spec_definition["name"]
    assert expert_agent.description == expert_spec_definition["description"]
    assert expert_agent.type == expert_spec_definition["type"]
    assert expert_agent.role == expert_spec_definition["role"]
    assert expert_agent.goal == expert_spec_definition["goal"]
    assert expert_agent.instructions == expert_spec_definition["instructions"]
    assert expert_agent.tools == expert_spec_definition["tools"]

@pytest.mark.asyncio
async def test_all_expert_agent_types_no_spec(expert_agent_for_all_types):
    _, expert_spec_definition = expert_agent_for_all_types

    expert_agent = ExpertAgent(
        name = expert_spec_definition["name"],
        description = expert_spec_definition["description"],
        type = expert_spec_definition["type"],
        role = expert_spec_definition["role"],
        goal = expert_spec_definition["goal"],
        instructions = expert_spec_definition["instructions"],
        tools = expert_spec_definition["tools"],
    )

    assert expert_agent.name == expert_spec_definition["name"]
    assert expert_agent.description == expert_spec_definition["description"]
    assert expert_agent.type == expert_spec_definition["type"]
    assert expert_agent.role == expert_spec_definition["role"]
    assert expert_agent.goal == expert_spec_definition["goal"]
    assert expert_agent.instructions == expert_spec_definition["instructions"]
    assert expert_agent.tools == expert_spec_definition["tools"]

@pytest.mark.asyncio
async def test_all_expert_agent_spec_validation(expert_agent_missing_values):
    agent_spec = expert_agent_missing_values["spec"]
    agent_type = expert_agent_missing_values["type"]
    missing_field = expert_agent_missing_values["missing"]

    try:
        _ = ExpertAgent(
            name = agent_spec.get("name", None),
            description = agent_spec.get("description", None),
            type = agent_spec.get("type", None),
            role = agent_spec.get("role", None),
            goal = agent_spec.get("goal", None),
            instructions = agent_spec.get("instructions", None),
            tools = agent_spec.get("tools", None),
        )
    except ValidationError as e:
        if missing_field == 'type' and "Value error, 'type' cannot be empty or just whitespace" in str(e):
            assert True
        elif "Input should be a valid string" in str(e):
            assert True
        else:
            assert False
