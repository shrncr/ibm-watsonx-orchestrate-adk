from ibm_watsonx_orchestrate.cli.commands.agents import agents_controller
from ibm_watsonx_orchestrate.agent_builder.agents.types import SupervisorConfig
import os
import json
from typer import BadParameter
from unittest.mock import patch
import pytest

@pytest.fixture
def expert_agent_content() -> dict:
    return {
            "name":"research_agent",
            "type":"expert",
            "description":"A Research Assistant which can query the web to help the user with research tasks that require current knowledge or open data from the web to complete.",
            "role":"You are a helpful and ethical AI research assistant that uses web search tools to answer user questions.",
            "goal":"Answer the user's question using the information found on the web.",
            "instructions":"Use the tools provided to answer the user's question.  If you do not have enough information to answer the question, say so.  If you need more information, ask follow up questions.",
            "tools":[
                "web_search"
            ]
        }

@pytest.fixture
def orchestrate_agent_content() -> dict:
    return {
            "name": "my_agent",
            "type": "orchestrator",
            "management_style": "supervisor",
            "management_style_config": {
                "reflection_enabled": True,
                "reflection_retry_count": 3
            },
            "llm": "granite",
            "agents": [
                "research_agent",
                "sales_agent"
            ]
        }


class MockSDKResponse:
    def __init__(self, response_obj):
        self.response_obj = response_obj

    def dumps_spec(self):
        return json.dumps(self.response_obj)

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.ExpertAgent")
def test_expert_agent_import_yaml(mock, capsys, expert_agent_content):
    mock.return_value = MockSDKResponse(expert_agent_content)
    file = os.path.join(os.path.dirname(__file__), "../../resources/yaml_samples/expert_agent.yaml")
    agents_controller.import_agent(file=file)
    captured = capsys.readouterr()
    print(captured.out)
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    assert mock.called
    assert json_captured["name"] == "research_agent"
    assert json_captured["type"] == "expert"
    assert json_captured["tools"] == ["web_search"]

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.ExpertAgent")
def test_expert_agent_import_json(mock, capsys, expert_agent_content):
    mock.return_value = MockSDKResponse(expert_agent_content)
    file = os.path.join(os.path.dirname(__file__), "../../resources/json_samples/expert_agent.json")
    agents_controller.import_agent(file=file)
    captured = capsys.readouterr()
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    assert mock.called
    assert json_captured["name"] == "research_agent"
    assert json_captured["type"] == "expert"
    assert json_captured["tools"] == ["web_search"]

def test_expert_agent_import_python(capsys):
    file = os.path.join(os.path.dirname(__file__), "../../resources/python_samples/base_expert_agent.py")
    agents_controller.import_agent(file=file)
    captured = capsys.readouterr()
    json_strs = captured.out.split("}\n{")
    json_strs[1] = "{" + str(json_strs[1]) + "}"
    json_strs[2] = "{" + str(json_strs[2])

    json_captured = [json.loads(x.replace("\n", "")) for x in json_strs[1:]]

    assert json_captured[1]["name"] == "research_agent"
    assert json_captured[1]["type"] == "expert"
    assert json_captured[1]["tools"] == ["myName"]

    assert json_captured[0]["name"] == "sample_orchestrator_agent"
    assert json_captured[0]["agents"] == ["research_agent"]

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.OrchestrateAgent")
def test_orchestrate_agent_import_yaml(mock, capsys, orchestrate_agent_content):
    mock.return_value = MockSDKResponse(orchestrate_agent_content)
    file = os.path.join(os.path.dirname(__file__), "../../resources/yaml_samples/orchestrator_agent.yaml")
    agents_controller.import_agent(file=file)
    captured = capsys.readouterr()
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    assert mock.called
    assert json_captured["name"] == "my_agent"
    assert json_captured["type"] == "orchestrator"
    assert json_captured["agents"] == ["research_agent", "sales_agent"]

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.OrchestrateAgent")
def test_orchestrate_agent_import_json(mock, capsys, orchestrate_agent_content):
    mock.return_value = MockSDKResponse(orchestrate_agent_content)
    file = os.path.join(os.path.dirname(__file__), "../../resources/json_samples/orchestrator_agent.json")
    agents_controller.import_agent(file=file)
    captured = capsys.readouterr()
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    assert mock.called
    assert json_captured["name"] == "my_agent"
    assert json_captured["type"] == "orchestrator"
    assert json_captured["agents"] == ["research_agent", "sales_agent"]


def test_agent_import_no_file():
    try:
        agents_controller.import_agent()
        assert False
    except TypeError:
        assert True

def test_agent_import_missing_file():
    try:
        agents_controller.import_agent(file="fake_file")
        assert False
    except FileNotFoundError:
        assert True

def test_agent_import_invalid_file_type():
    try:
        agents_controller.import_agent(file=os.path.join(os.path.dirname(__file__), "../../resources/misc/sample.txt"))
        assert False
    except ValueError as e:
        assert "file must end in .json, .yaml, .yml or .py" in str(e)
        assert True

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.yaml.load")
def test_agent_import_invaild_type(mock):
    mock.return_value = { "type" : "fake"}
    file = os.path.join(os.path.dirname(__file__), "../../resources/yaml_samples/orchestrator_agent.yaml")
    try:
        agents_controller.import_agent(file=file)
        assert False
    except ValueError as e:
        assert "'type' must be either orchestrator or expert" in str(e)
        assert True

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.ExpertAgent")
def test_expert_agent_create(mock, capsys, expert_agent_content):
    mock.return_value = MockSDKResponse(expert_agent_content)

    agents_controller.create_agent(
        name="research_agent",
        type=agents_controller.AgentTypes("expert"),
        description="Test for expert agent description",
        role="Test for expert agent role",
        goal="Test for expert agent goal",
        instructions="Test for expert agent instructions",
        tools="web_search, test_tool_2",
        )
    captured = capsys.readouterr()
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    mock.assert_called_once_with(
            name="research_agent",
            type="expert",
            description="Test for expert agent description",
            role="Test for expert agent role",
            goal="Test for expert agent goal",
            instructions="Test for expert agent instructions",
            tools=["web_search", "test_tool_2"],
        )
    assert json_captured["name"] == "research_agent"
    assert json_captured["type"] == "expert"
    assert json_captured["tools"] == ["web_search"]

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.ExpertAgent")
def test_expert_agent_create_missing_args(mock, capsys, expert_agent_content):
    mock.return_value = MockSDKResponse(expert_agent_content)
    try:
        agents_controller.create_agent(
            name="",
            type=agents_controller.AgentTypes("expert"),
            description=None,
            role=None,
            goal=None,
            instructions=None,
            tools=None,
            )
        assert False
    except BadParameter as e:
        assert "role" in e.message
        assert "goal" in e.message
        assert "instructions" in e.message
        assert "tools" in e.message

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.OrchestrateAgent")
def test_orchestrator_agent_create(mock, capsys, orchestrate_agent_content):
    mock.return_value = MockSDKResponse(orchestrate_agent_content)

    agents_controller.create_agent(
        name="my_agent",
        type=agents_controller.AgentTypes("orchestrator"),
        management_style="supervisor",
        management_style_config="reflection_enabled=true,reflection_retry_count=3",
        llm="granite",
        agents="research_agent, sales_agent"
        )
    captured = capsys.readouterr()
    print(str(captured.out))
    json_captured = json.loads(str(captured.out).replace("\n", ""))

    mock.assert_called_once_with(
            name="my_agent",
            management_style="supervisor",
            management_style_config=SupervisorConfig(reflection_enabled=True, reflection_retry_count=3),
            llm="granite",
            agents=["research_agent", "sales_agent"]
        )
    assert json_captured["name"] == "my_agent"
    assert json_captured["type"] == "orchestrator"
    assert json_captured["agents"] == ["research_agent", "sales_agent"]

@patch("ibm_watsonx_orchestrate.cli.commands.agents.agents_controller.OrchestrateAgent")
def test_orchestrator_agent_create_no_args(mock, orchestrate_agent_content):
    mock.return_value = MockSDKResponse(orchestrate_agent_content)

    try:
        agents_controller.create_agent(
            name="",
            type=agents_controller.AgentTypes("orchestrator"),
            management_style=None,
            management_style_config=None,
            llm=None,
            agents=None
            )
        assert False
    except BadParameter as e:
        assert "agents" in e.message