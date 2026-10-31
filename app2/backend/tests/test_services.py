import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from openai import APIConnectionError, APIStatusError, APITimeoutError

import services
from models import SummaryLength


def make_choice_content(content: str):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


def test_resumir_returns_valid_response(monkeypatch):
    payload = {
        "summary": "Resumen de prueba",
        "main_ideas": ["Idea principal", "Idea secundaria"],
        "glossary": [{"concept": "IA", "definition": "Inteligencia artificial"}],
    }
    mock_create = Mock(return_value=make_choice_content(json.dumps(payload)))
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    result = services.resumir("Texto de prueba", True, True, SummaryLength.STANDARD)

    assert result.summary == payload["summary"]
    assert result.main_ideas == payload["main_ideas"]
    assert result.glossary[0].concept == "IA" # type: ignore
    mock_create.assert_called_once()


def test_resumir_raises_timeout_error(monkeypatch):
    mock_create = Mock(side_effect=APITimeoutError(request=Mock()))
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IATimeoutError):
        services.resumir("Texto de prueba", False, False, SummaryLength.BRIEF)


def test_resumir_raises_provider_error_on_connection_issue(monkeypatch):
    mock_create = Mock(
        side_effect=APIConnectionError(message="connection failed", request=Mock())
    )
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IAProveedorError):
        services.resumir("Texto de prueba", False, False, SummaryLength.STANDARD)


def test_resumir_raises_provider_error_on_status_error(monkeypatch):
    mock_create = Mock(
        side_effect=APIStatusError(
            "provider error",
            response=Mock(status_code=500),
            body=None,
        )
    )
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IAProveedorError):
        services.resumir("Texto de prueba", False, False, SummaryLength.STANDARD)


def test_resumir_raises_for_empty_response(monkeypatch):
    mock_create = Mock(return_value=make_choice_content("   "))
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IARespuestaInvalidaError):
        services.resumir("Texto de prueba", False, False, SummaryLength.STANDARD)


def test_resumir_raises_for_invalid_json(monkeypatch):
    mock_create = Mock(return_value=make_choice_content("{no es json}"))
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IARespuestaInvalidaError):
        services.resumir("Texto de prueba", False, False, SummaryLength.STANDARD)


def test_resumir_raises_for_invalid_schema(monkeypatch):
    mock_create = Mock(return_value=make_choice_content(json.dumps({"main_ideas": ["Idea principal"]})))
    monkeypatch.setattr(services.client.chat.completions, "create", mock_create, raising=False)

    with pytest.raises(services.IARespuestaInvalidaError):
        services.resumir("Texto de prueba", True, False, SummaryLength.STANDARD)
