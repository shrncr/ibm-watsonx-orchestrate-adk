from ibm_watsonx_orchestrate.client.base_api_client import BaseAPIClient


class ExpertAgentClient(BaseAPIClient):
    """
    Client to handle CRUD operations for Expert Agent endpoint
    """

    def create(self, payload: dict) -> dict:
        return self._post("/agents/expert", data=payload)

    def get(self) -> dict:
        return self._get("/agents/expert")

    def update(self, agent_id: str, data: dict) -> dict:
        return self._patch(f"/agents/expert/{agent_id}", data=data)

    def delete(self, agent_id: str) -> dict:
        return self._delete(f"/agents/expert/{agent_id}")