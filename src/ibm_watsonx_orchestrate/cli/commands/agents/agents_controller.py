import yaml
import json
import rich
import re
import typer
import importlib
import inspect
import sys
from pathlib import Path
from enum import Enum
from ibm_watsonx_orchestrate.cli.commands.tools.tools_controller import import_python_tool
from ibm_watsonx_orchestrate.agent_builder.agents.expert_agent import ExpertAgent
from ibm_watsonx_orchestrate.agent_builder.agents.orchestrate_agent import OrchestrateAgent
from ibm_watsonx_orchestrate.agent_builder.agents.types import SupervisorConfig, ExpertAgentType
DEFAULT_REFLECTION_RETRY_COUNT_WHEN_ENABLED = 3

class AgentTypes(str, Enum):
    expert = "expert"
    orchestrator = "orchestrator"

def import_python_agent(file: str) -> list[ExpertAgent | OrchestrateAgent]:
    # Import tools
    import_python_tool(file)

    file_path = Path(file)
    file_directory = file_path.parent
    file_name = file_path.stem
    sys.path.append(str(file_directory))
    module = importlib.import_module(file_name)
    del sys.path[-1]
    
    agents = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, ExpertAgent) or isinstance(obj, OrchestrateAgent):
            agents.append(obj)
    return agents

def create_agent_from_spec(agent_details:dict) -> ExpertAgent | OrchestrateAgent:
    match agent_details["type"]:
        case "orchestrator":
            agent_details.pop('type', None)
            agent = OrchestrateAgent(**agent_details)
        case x if x in [e.value for e in ExpertAgentType]:
            agent = ExpertAgent(**agent_details)
        case _:
            raise ValueError("'type' must be either orchestrator or expert")
    
    return agent

def parse_file(file: str) -> list[ExpertAgent | OrchestrateAgent]:
    with open(file, 'r') as f:
        if file.endswith('.yaml') or file.endswith('.yml'):
            content = yaml.load(f, Loader=yaml.SafeLoader)
            agent = create_agent_from_spec(content)
            return [agent]
        elif file.endswith('.json'):
            content = json.load(f)
            agent = create_agent_from_spec(content)
            return [agent]
        elif file.endswith('.py'):
            agents = import_python_agent(file)
            return agents
        else:
            raise ValueError('file must end in .json, .yaml, .yml or .py')

def parse_create_expert_args(name: str, type: AgentTypes, **args) -> dict:
    agent_details = {
        "name": name,
        "type": type,
        "description": args.get("description", ""),
        "role": args.get("role", None),
        "goal": args.get("goal", None),
        "instructions": args.get("instructions", None)
    }

    tools = args.get("tools", "")

    tools = [x.strip() for x in tools.split(",")] if tools is not None else []
    agent_details["tools"] = tools
    return agent_details

def parse_create_orchestrator_args(name: str, **args) -> dict:
    agent_details = {
        "name": name,
        "management_style": args.get("management_style", ""),
        "llm": args.get("llm", None)
    }

    agent_details["management_style_config"] = None

    if "management_style_config" in args and args["management_style_config"]:
        management_style_config = args["management_style_config"]
        config = {}
        for kv_pair in management_style_config.split(","):
            k, v = kv_pair.split("=")
            k, v = k.strip(), v.strip()
            if k == "reflection_enabled":
                v = v.lower() == "true"
            if k == "reflection_retry_count":
                try:
                    v = int(v)
                except ValueError as e:
                    raise ValueError(f"{v} is not a valid retry count")
            config[k] = v
        if (
            config.get("reflection_enabled", False)
            and "reflection_retry_count" not in config
        ):
            config[
                "reflection_retry_count"
            ] = DEFAULT_REFLECTION_RETRY_COUNT_WHEN_ENABLED

        supervisor_config = SupervisorConfig(**config)
        agent_details["management_style_config"] = supervisor_config

    agents = args.get("agents", "")
    agents = [x.strip() for x in agents.split(",")] if agents is not None else []
    agent_details["agents"] = agents
    return agent_details

def validate_create_expert_args(name: str, type: AgentTypes, **args) -> None:
    missing_params = []
    if args["role"] is None or len(args["role"]) == 0:
        missing_params.append("--role")
    if args["goal"] is None or len(args["goal"]) == 0:
        missing_params.append("--goal")
    if args["instructions"] is None or len(args["instructions"]) == 0:
        missing_params.append("--instructions")
    if type.value == 'expert' and (args["tools"] is None or len(args["tools"]) == 0):
        missing_params.append("--tools")

    if len(missing_params) > 0:
        raise typer.BadParameter(
            f"Missing flags {missing_params} required for type '{type.value}'. These value cannot be missing or empty."
        )

def validate_create_orchestrator_args(name: str, **args) -> None:
    missing_params = []
    if args["agents"] is None or len(args["agents"]) == 0:
        missing_params.append("--agents")

    if len(missing_params) > 0:
        raise typer.BadParameter(
            f"Missing flags {missing_params} required for type 'orchestrator'. These value cannot be missing ot empty."
        )

def import_agent(file: str) -> None:

    agents = parse_file(file)
    for agent in agents:
        rich.print(agent.dumps_spec())

def create_agent(name: str, type: AgentTypes, **kwargs) -> None:
    match type.value:
        case "orchestrator":
            validate_create_orchestrator_args(name, **kwargs)
            agent_details = parse_create_orchestrator_args(name,  **kwargs)
            agent = OrchestrateAgent(**agent_details)
        case x if x in [e.value for e in ExpertAgentType]:
            validate_create_expert_args(name, type, **kwargs)
            agent_details = parse_create_expert_args(name, type, **kwargs)
            agent = ExpertAgent(**agent_details)
        case _:
            raise ValueError("'type' must be either orchestrator or expert")
    
    rich.print(agent.dumps_spec())

    if "output_file" in kwargs and kwargs["output_file"] is not None:
        agent.dump_spec(kwargs["output_file"])
