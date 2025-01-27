from ibm_watsonx_orchestrate.client.utils import instantiate_client
from ibm_watsonx_orchestrate.client import utils
from ibm_watsonx_orchestrate.client.agents.orchestrator_agent_client import OrchestratorAgentClient
from ibm_watsonx_orchestrate.client.agents.expert_agent_client import ExpertAgentClient


def test_expert_client():
    utils.DEFAULT_CONFIG_FILE_FOLDER = "tests/client/resources/"
    utils.DEFAULT_CONFIG_FILE = "config.yaml"
    utils.AUTH_CONFIG_FILE_FOLDER = "tests/client/resources/"
    utils.AUTH_CONFIG_FILE = "credentials.yaml"

    client = instantiate_client(ExpertAgentClient)
    assert client


def test_orchestrate_client():
    utils.DEFAULT_CONFIG_FILE_FOLDER = "tests/client/resources/"
    utils.DEFAULT_CONFIG_FILE = "config.yaml"
    utils.AUTH_CONFIG_FILE_FOLDER = "tests/client/resources/"
    utils.AUTH_CONFIG_FILE = "credentials.yaml"

    client = instantiate_client(OrchestratorAgentClient)
    assert client