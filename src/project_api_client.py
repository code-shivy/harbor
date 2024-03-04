#Implement an asynchronous method for listing projects.
from base_api_client import BaseHarborApiClient

class ProjectApiClient(BaseHarborApiClient):
    async def list_projects(self):
        return await self.get('/api/projects')
