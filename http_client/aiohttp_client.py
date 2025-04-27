from http_client.request_executor import async_request_executor


class HttpClient:
    @staticmethod
    @async_request_executor()
    async def get_apod(response, *, url: str):
        return await response.json()
