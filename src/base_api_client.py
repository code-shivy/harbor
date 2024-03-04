# base_api_client.py
import httpx
from httpx import HTTPError
from tenacity import retry, stop_after_attempt, wait_fixed

class BaseHarborApiClient:
    def __init__(self, base_url, username, password):
        self.base_url = os.getenv('HARBOR_API_URL')
        self.username = os.getenv('HARBOR_USERNAME')
        self.password = os.getenv('HARBOR_PASSWORD')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def get(self, endpoint, params=None):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url + endpoint, params=params, auth=(self.username, self.password))
                response.raise_for_status()
                return response.json()
            except (HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
                raise Exception(f"Failed to make GET request to {endpoint}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def post(self, endpoint, data=None):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url + endpoint, json=data, auth=(self.username, self.password))
                response.raise_for_status()
                return response.json()
            except (HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
                raise Exception(f"Failed to make POST request to {endpoint}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def put(self, endpoint, data=None):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(self.base_url + endpoint, json=data, auth=(self.username, self.password))
                response.raise_for_status()
                return response.json()
            except (HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
                raise Exception(f"Failed to make PUT request to {endpoint}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def delete(self, endpoint):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(self.base_url + endpoint, auth=(self.username, self.password))
                response.raise_for_status()
                return response.json()
            except (HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
                raise Exception(f"Failed to make DELETE request to {endpoint}: {e}")
