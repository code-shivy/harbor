## The entry point of your application. Contains the main function where you instantiate and use your
##Harbor API client.
# main.py
import asyncio
from dotenv import load_dotenv
from src.base_api_client import BaseHarborApiClient
from src.project_api_client import ProjectApiClient
from src.repository_api_client import RepositoryApiClient
from src.artifact_api_client import ArtifactApiClient

async def main():
    # Instantiate Harbor API clients
    base_api_client = BaseHarborApiClient(
        os.getenv('HARBOR_API_URL'),
        os.getenv('HARBOR_USERNAME'),
        os.getenv('HARBOR_PASSWORD')
    )
    project_api_client = ProjectApiClient(base_api_client)
    repository_api_client = RepositoryApiClient(base_api_client)
    artifact_api_client = ArtifactApiClient(base_api_client)

    #  List projects
    projects = await project_api_client.list_projects()
    print("Projects:")
    for project in projects:
        print(project['name'])

    #  List repositories within a project
    project_name = "my_project"
    repositories = await repository_api_client.list_repositories(project_name)
    print(f"Repositories in project '{project_name}':")
    for repo in repositories:
        print(repo['name'])

    #  List artifacts within a repository
    repository_name = "my_repository"
    artifacts = await artifact_api_client.list_artifacts(project_name, repository_name)
    print(f"Artifacts in repository '{repository_name}':")
    for artifact in artifacts:
        print(artifact['name'])

    #  Delete old tags in a repository
    await artifact_api_client.delete_old_tags(project_name, repository_name)
    print(f"Old tags in repository '{repository_name}' deleted.")

if __name__ == "__main__":
    asyncio.run(main())
