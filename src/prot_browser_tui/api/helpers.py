
from typing import Any


def get_organism_name(entry: dict[str, Any]) -> str:
    if "scientificName" in entry["organism"]:
        if "commonName" in entry["organism"]:
            return f"{entry["organism"]["scientificName"]} ({entry["organism"]["commonName"]})"
        else:
            return entry["organism"]["scientificName"]
    else:
        if "commonName" in entry["organism"]:
            return entry["organism"]["commonName"]
        else:
            return "N/A"


def get_recommended_name(entry: dict[str, Any]) -> str:
    if "recommendedName" in entry["proteinDescription"]:
        return entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
    else:
        return "N/A"
