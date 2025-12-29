import os
import aiohttp


async def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Async main function for text generation tasks."""

    url = os.getenv("WEBHOOK_URL")

    if not url:
        raise ValueError("WEBHOOK_URL environment variable is not set.")

    headers = {
        "Content-Type": "application/json"
    }

    params = {"prompt": prompt}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                error_text = await response.text()
                return {
                    "error": f"Request failed with status {response.status}: {error_text}"
                }
