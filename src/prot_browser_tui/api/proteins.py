import asyncio
from types import CoroutineType
from typing import Any
import httpx

uniprot_api_url: str = "https://rest.uniprot.org/uniprotkb/search"

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
                "Organism name": f"{entry["organism"]["scientificName"]} ({entry["organism"]["commonName"]})",
                "Common Name": entry["proteinDescription"]["recommendedName"]["fullName"]["value"],
                                                }
        entry_count += 1

    return display_data


if __name__ == "__main__":
    response = asyncio.run(get_search_results(uniprot_api_url, "insulin"))
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
