# artifact_api_client.py
import httpx
import asyncio
from datetime import datetime, timedelta
import os
from base_api_client import BaseHarborApiClient

class ArtifactApiClient(BaseHarborApiClient):
    async def list_artifacts(self, project_name, repository_name):
        return await self.get(f'/api/artifacts?project_name={project_name}&repository_name={repository_name}')

    async def delete_old_images(self, project_name, repository_name):
        artifacts = await self.list_artifacts(project_name, repository_name)
        for artifact in artifacts:
            for tag in artifact['tags']:
                if self._is_old_image(tag['created']):
                    await self.delete_image(project_name, repository_name, tag['name'])

    async def delete_image(self, project_name, repository_name, tag_name):
        await self.delete(f'/api/artifacts/{project_name}/{repository_name}/tags/{tag_name}')

    def _is_old_image(self, created_timestamp):
        # Convert created_timestamp to datetime object
        created_date = datetime.fromtimestamp(created_timestamp)
        # Calculate the difference between current date and created date
        difference = datetime.now() - created_date
        # Return True if the difference is greater than 30 days
        return difference.days > 30

async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Instantiate Harbor API client
    artifact_api_client = ArtifactApiClient()

    # Delete old images
    await artifact_api_client.delete_old_images(os.getenv('HARBOR_PROJECT_NAME'), os.getenv('HARBOR_REPOSITORY_NAME'))

if __name__ == "__main__":
    asyncio.run(main())
