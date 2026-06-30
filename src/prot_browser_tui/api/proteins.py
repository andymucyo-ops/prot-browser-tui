from typing import Any
import httpx
# import asyncio

base_url: str = "https://rest.uniprot.org/uniprotkb/search"

def get_status_code(url: str, prot_name: str) -> int:
    response: httpx.Response = httpx.get(
            url,
            params=[
                ("query","insulin"),
                ],
            headers={
                "Content-Type": "application/json"
                }
            )
    
    return response.status_code

def get_search_results(url: str, prot_name: str) -> dict[Any,Any] :
    payload = {
            "query": prot_name,
            "size": 1,
            "fields": ["accession", "id", "protein_name", "organism_name"],
            }
    response: httpx.Response = httpx.get(
            url,
            params= payload,
            headers={
                "Content-Type": "application/json"
                }
            )
    
    return response.json()["results"][0]



if __name__ == "__main__":
    print("Status code: ",get_status_code(base_url, "insulin"))
    print("json: ", get_search_results(base_url, "insulin"))

