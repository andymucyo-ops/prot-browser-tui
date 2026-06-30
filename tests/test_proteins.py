import json
from typing import Any

import httpx
import pytest
import respx

from prot_browser_tui import extract_display_data, get_search_results
from prot_browser_tui.api import uniprot_api_url


class TestExtractDisplayData:
    def test_single_entry(
        self,
        mock_protein_insulin: dict[str, Any],
    ) -> None:
        data = extract_display_data([mock_protein_insulin])

        assert len(data) == 1
        entry = data["entry n°1"]
        assert entry["Accession"] == "P01308"
        assert entry["UniprotKB ID"] == "INS_HUMAN"
        assert entry["Organism name"] == "Homo sapiens (Human)"
        assert entry["Common Name"] == "Insulin"

    def test_multiple_entries(
        self,
        mock_protein_insulin: dict[str, Any],
        mock_protein_albumin: dict[str, Any],
        mock_protein_actin: dict[str, Any],
    ) -> None:
        data = extract_display_data(
            [mock_protein_insulin, mock_protein_albumin, mock_protein_actin],
        )

        assert len(data) == 3
        assert data["entry n°1"]["Accession"] == "P01308"
        assert data["entry n°2"]["Accession"] == "P02768"
        assert data["entry n°3"]["Accession"] == "P60709"

    def test_empty_list(self) -> None:
        assert extract_display_data([]) == {}

    def test_missing_organism_common_name(
        self,
        mock_protein_missing_common_name: dict[str, Any],
    ) -> None:
        with pytest.raises(KeyError):
            extract_display_data([mock_protein_missing_common_name])

    def test_missing_recommended_name(
        self,
        mock_protein_missing_recommended_name: dict[str, Any],
    ) -> None:
        with pytest.raises(KeyError):
            extract_display_data([mock_protein_missing_recommended_name])


class TestGetSearchResults:
    async def test_search_success(
        self,
        respx_mock: respx.MockRouter,
        mock_search_response: dict[str, Any],
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(
            status_code=200,
            json=mock_search_response,
        )
        results = await get_search_results(uniprot_api_url, "insulin")

        assert len(results) == 2
        assert results[0]["primaryAccession"] == "P01308"
        assert results[1]["primaryAccession"] == "P02768"

    async def test_search_sends_correct_params(
        self,
        respx_mock: respx.MockRouter,
        mock_search_response: dict[str, Any],
    ) -> None:
        route = respx_mock.get(uniprot_api_url).respond(
            status_code=200,
            json=mock_search_response,
        )
        await get_search_results(uniprot_api_url, "ferritin", size=10)

        request = route.calls.last.request
        assert request.url.params["query"] == "ferritin"
        assert request.url.params["facets"] == "reviewed"
        assert request.url.params["size"] == "10"

    async def test_search_zero_results(
        self,
        respx_mock: respx.MockRouter,
        mock_empty_response: dict[str, Any],
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(
            status_code=200,
            json=mock_empty_response,
        )
        results = await get_search_results(uniprot_api_url, "nonexistent")
        assert results == []

    async def test_search_http_404(
        self,
        respx_mock: respx.MockRouter,
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(status_code=404)
        with pytest.raises(httpx.HTTPStatusError):
            await get_search_results(uniprot_api_url, "test")

    async def test_search_http_500(
        self,
        respx_mock: respx.MockRouter,
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(status_code=500)
        with pytest.raises(httpx.HTTPStatusError):
            await get_search_results(uniprot_api_url, "test")

    async def test_search_connection_error(
        self,
        respx_mock: respx.MockRouter,
    ) -> None:
        respx_mock.get(uniprot_api_url).mock(
            side_effect=httpx.ConnectError("connection refused"),
        )
        with pytest.raises(httpx.ConnectError):
            await get_search_results(uniprot_api_url, "test")

    async def test_search_timeout(
        self,
        respx_mock: respx.MockRouter,
    ) -> None:
        respx_mock.get(uniprot_api_url).mock(
            side_effect=httpx.TimeoutException("timed out"),
        )
        with pytest.raises(httpx.TimeoutException):
            await get_search_results(uniprot_api_url, "test")

    async def test_search_malformed_json(
        self,
        respx_mock: respx.MockRouter,
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(
            status_code=200,
            content=b"not valid json",
        )
        with pytest.raises(json.JSONDecodeError):
            await get_search_results(uniprot_api_url, "test")


class TestIntegration:
    async def test_extract_from_search(
        self,
        respx_mock: respx.MockRouter,
        mock_single_result: dict[str, Any],
    ) -> None:
        respx_mock.get(uniprot_api_url).respond(
            status_code=200,
            json=mock_single_result,
        )
        results = await get_search_results(uniprot_api_url, "insulin")
        data = extract_display_data(results)

        assert len(data) == 1
        entry = data["entry n°1"]
        assert entry["Accession"] == "P01308"
        assert entry["UniprotKB ID"] == "INS_HUMAN"
        assert entry["Organism name"] == "Homo sapiens (Human)"
        assert entry["Common Name"] == "Insulin"
