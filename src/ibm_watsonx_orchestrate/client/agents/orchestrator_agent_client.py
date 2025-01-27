from ibm_watsonx_orchestrate.client.base_api_client import BaseAPIClient


class OrchestratorAgentClient(BaseAPIClient):
    """
    Client to handle CRUD operations for Orchestrator Agent endpoint
    """

    def create(self, payload: dict) -> dict:
        return self._post("/agents/orchestrator-agent", data=payload)

    def get(self) -> dict:
        return self._get("/agents/orchestrator-agent")

    def update(self, agent_id: str, data: dict) -> dict:
        return self._patch(f"/agents/orchestrator-agent/{agent_id}", data=data)

    def delete(self, agent_id: str) -> dict:
        return self._delete(f"/agents/orchestrator-agent/{agent_id}")