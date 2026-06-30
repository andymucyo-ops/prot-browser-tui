import asyncio
from types import CoroutineType
from typing import Any
import httpx

uniprot_api_url: str = "https://rest.uniprot.org/uniprotkb/search"

async def get_search_results(url: str, prot_name: str, size: int=5) -> dict[str, Any] :
    payload = {
            "query": prot_name,
            "size": 1,
            "fields": ["accession", "id", "protein_name", "organism_name"],
            }
    async with httpx.AsyncClient() as client:
        response: CoroutineType = await client.get(
                url,
                params= payload,
                headers={
                    "Content-Type": "application/json"
                    }
                )
        
        print("status code: ", response.status_code)
        return response.json()["results"][0]



if __name__ == "__main__":
    # print("Status code: ",get_status_code(uniprot_api_url, "insulin"))
    print(asyncio.run(get_search_results(uniprot_api_url, "insulin")))
