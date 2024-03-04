#Contains the RepositoryApiClient class.
from base_api_client import BaseHarborApiClient

class RepositoryApiClient(BaseHarborApiClient):
    async def list_repositories(self, project_name):
        return await self.get(f'/api/repositories?project_name={project_name}')
