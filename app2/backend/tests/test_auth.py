import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from jwt.exceptions import PyJWKClientConnectionError, PyJWKClientError

import main
from models import SummaryLength


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_missing_authorization_is_rejected_before_body_validation(
    app_client, summary_service
):
    response = app_client.post(
        "/resumir",
        content=b"{malformed json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_invalid_authorization_is_rejected_before_body_validation(
    app_client, summary_service, configure_jwks
):
    configure_jwks()
    response = app_client.post(
        "/resumir",
        content=b"{malformed json",
        headers={"Content-Type": "application/json", **bearer("not-a-jwt")},
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


@pytest.mark.parametrize(
    "authorization",
    ["Basic credentials", "Bearer ", "Bearer\tinvalid"],
)
def test_unusable_bearer_header_is_rejected(app_client, summary_service, authorization):
    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers={"Authorization": authorization},
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_malformed_token_is_rejected(app_client, summary_service, configure_jwks):
    configure_jwks()

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer("not-a-jwt"),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_invalid_signature_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    from cryptography.hazmat.primitives.asymmetric import rsa

    configure_jwks()
    other_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    token = issue_token(signing_key=other_private_key)

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_wrong_issuer_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    configure_jwks()
    token = issue_token(issuer="https://wrong-issuer.test")

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_expired_token_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    configure_jwks()
    token = issue_token(expires_at=datetime.now(timezone.utc) - timedelta(minutes=1))

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_token_without_expiration_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    configure_jwks()
    token = issue_token(include_exp=False)

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_unmatched_signing_key_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    configure_jwks()
    token = issue_token(kid="unknown-key")

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_future_not_before_claim_is_rejected(
    app_client, summary_service, configure_jwks, issue_token
):
    configure_jwks()
    token = issue_token(not_before=datetime.now(timezone.utc) + timedelta(minutes=5))

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


def test_non_rs256_token_is_rejected(app_client, summary_service):
    token = jwt.encode(
        {
            "iss": os.environ["CLERK_ISSUER"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        "untrusted-secret-at-least-32-bytes",
        algorithm="HS256",
        headers={"kid": "test-key"},
    )

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 401
    summary_service.assert_not_called()


@pytest.mark.parametrize(
    "failure",
    [
        PyJWKClientConnectionError("JWKS connection failed"),
        PyJWKClientConnectionError("JWKS request timed out"),
        PyJWKClientError("JWKS has no usable signing keys"),
    ],
)
def test_jwks_unavailability_returns_503_without_summary(
    app_client, summary_service, configure_jwks, issue_token, failure
):
    configure_jwks(error=failure)
    token = issue_token()

    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(token),
    )

    assert response.status_code == 503
    assert token not in response.text
    summary_service.assert_not_called()


def test_missing_issuer_configuration_fails_closed(
    app_client, summary_service, issue_token, monkeypatch
):
    monkeypatch.setenv("CLERK_ISSUER", "")
    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(issue_token()),
    )

    assert response.status_code == 503
    summary_service.assert_not_called()


@pytest.mark.parametrize("timeout", ["nan", "inf", "0", "-1"])
def test_non_finite_or_non_positive_jwks_timeout_fails_closed(
    app_client, summary_service, issue_token, monkeypatch, timeout
):
    monkeypatch.setenv("CLERK_JWKS_TIMEOUT", timeout)
    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers=bearer(issue_token()),
    )

    assert response.status_code == 503
    summary_service.assert_not_called()


def test_valid_token_preserves_summary_contract_and_calls_service_once(
    app_client, summary_service, configure_jwks, issue_token, caplog
):
    configure_jwks()
    token = issue_token()
    request_body = {"text": "texto de prueba", "main_ideas": True}

    response = app_client.post(
        "/resumir", json=request_body, headers=bearer(token)
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Resumen de prueba",
        "main_ideas": ["Idea de prueba"],
    }
    assert token not in response.text
    assert token not in caplog.text
    summary_service.assert_called_once_with(
        "texto de prueba",
        True,
        False,
        SummaryLength.STANDARD,
    )


def test_authorization_cors_preflight_is_allowed(app_client):
    response = app_client.options(
        "/resumir",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )

    assert response.status_code == 200
    assert "authorization" in response.headers["access-control-allow-headers"].lower()


def test_auth_error_responses_include_cors_headers(app_client, summary_service):
    response = app_client.post(
        "/resumir",
        json={"text": "texto de prueba"},
        headers={
            "Origin": "http://localhost:5173",
            "Authorization": "Bearer not-a-jwt",
        },
    )

    assert response.status_code == 401
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    summary_service.assert_not_called()


def test_health_endpoint_is_public_and_returns_ok(app_client):
    response = app_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
