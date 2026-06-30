from typing import Any

import pytest
import respx


@pytest.fixture
def mock_protein_insulin() -> dict[str, Any]:
    return {
        "primaryAccession": "P01308",
        "uniProtkbId": "INS_HUMAN",
        "organism": {
            "scientificName": "Homo sapiens",
            "commonName": "Human",
        },
        "proteinDescription": {
            "recommendedName": {
                "fullName": {"value": "Insulin"},
            },
        },
    }


@pytest.fixture
def mock_protein_albumin() -> dict[str, Any]:
    return {
        "primaryAccession": "P02768",
        "uniProtkbId": "ALBU_HUMAN",
        "organism": {
            "scientificName": "Homo sapiens",
            "commonName": "Human",
        },
        "proteinDescription": {
            "recommendedName": {
                "fullName": {"value": "Serum albumin"},
            },
        },
    }


@pytest.fixture
def mock_protein_actin() -> dict[str, Any]:
    return {
        "primaryAccession": "P60709",
        "uniProtkbId": "ACTB_HUMAN",
        "organism": {
            "scientificName": "Homo sapiens",
            "commonName": "Human",
        },
        "proteinDescription": {
            "recommendedName": {
                "fullName": {"value": "Actin, cytoplasmic 1"},
            },
        },
    }


@pytest.fixture
def mock_protein_missing_common_name() -> dict[str, Any]:
    return {
        "primaryAccession": "Q9Y261",
        "uniProtkbId": "FOXA2_HUMAN",
        "organism": {
            "scientificName": "Homo sapiens",
        },
        "proteinDescription": {
            "recommendedName": {
                "fullName": {"value": "Hepatocyte nuclear factor 3-beta"},
            },
        },
    }


@pytest.fixture
def mock_protein_missing_recommended_name() -> dict[str, Any]:
    return {
        "primaryAccession": "P12345",
        "uniProtkbId": "UNK_HUMAN",
        "organism": {
            "scientificName": "Homo sapiens",
            "commonName": "Human",
        },
        "proteinDescription": {},
    }


@pytest.fixture
def mock_search_response(
    mock_protein_insulin: dict[str, Any],
    mock_protein_albumin: dict[str, Any],
) -> dict[str, Any]:
    return {"results": [mock_protein_insulin, mock_protein_albumin]}


@pytest.fixture
def mock_empty_response() -> dict[str, Any]:
    return {"results": []}


@pytest.fixture
def mock_single_result(
    mock_protein_insulin: dict[str, Any],
) -> dict[str, Any]:
    return {"results": [mock_protein_insulin]}


@pytest.fixture
def respx_mock() -> respx.MockRouter:
    with respx.mock as mock:
        yield mock
