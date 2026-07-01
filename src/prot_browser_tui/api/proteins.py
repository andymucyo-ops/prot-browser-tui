import asyncio
from types import CoroutineType
from typing import Any
import httpx

from .helpers import get_organism_name, get_recommended_name

UNIPROT_API_URL: str = "https://rest.uniprot.org/uniprotkb/search"

async def get_search_results(url: str, prot_name: str, size: int=5) -> dict[str, Any] :
    payload = {
            "query": prot_name,
            "facets": "reviewed",
            "size": size,
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
        response.raise_for_status()
        return response.json()["results"]


def extract_display_data(response_json: dict[str: Any]):
    display_data: dict[str, dict[str, str]] = {}
    entry_count: int = 1

    for entry in response_json:
        display_data[f"entry n°{entry_count}"] = {
                "Accession": entry["primaryAccession"], 
                "UniprotKB ID": entry["uniProtkbId"],
                "Organism Name": get_organism_name(entry),
                "Common Name": get_recommended_name(entry),
                                                }
        entry_count += 1

    return display_data

def get_accssion_id(entry: dict[str, Any]) -> str:
    pass

async def get_single_protein_data(url: str, accession_id: str) -> dict[str, Any]:
    pass


if __name__ == "__main__":
    response = asyncio.run(get_search_results(UNIPROT_API_URL, "insulin"))
    display_data = extract_display_data(response)

    for key in display_data.keys():
        print(f"{key}: {display_data[key]}")
    

    # for i in range(0, len(response)):
    #     entry = response[i]
    #     print("--------------")
    #     print(f"entry n°{i + 1}")
    #     print("--------------")
    #     for key in entry.keys():
    #         print(f"{key}: {entry[key]}\n")
