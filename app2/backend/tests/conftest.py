import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
os.environ["CLERK_ISSUER"] = "https://issuer.test"
os.environ["CLERK_JWKS_URL"] = "https://issuer.test/.well-known/jwks.json"
os.environ["CLERK_JWKS_TIMEOUT"] = "1"

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))
import auth
import main

ISSUER = os.environ["CLERK_ISSUER"]


@pytest.fixture(scope="session")
def rsa_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


@pytest.fixture
def issue_token(rsa_key_pair):
    private_key, _ = rsa_key_pair

    def issue(
        *,
        kid="test-key",
        issuer=ISSUER,
        not_before=None,
        expires_at=None,
        include_exp=True,
        signing_key=None,
    ):
        now = datetime.now(timezone.utc)
        claims = {
            "iss": issuer,
            "sub": "test-user",
            "nbf": not_before or now - timedelta(seconds=1),
        }
        if include_exp:
            claims["exp"] = expires_at or now + timedelta(minutes=5)
        return jwt.encode(
            claims,
            signing_key or private_key,
            algorithm="RS256",
            headers={"kid": kid},
        )

    return issue


@pytest.fixture
def configure_jwks(monkeypatch, rsa_key_pair):
    _, public_key = rsa_key_pair

    def install(*, error=None, keys=None):
        class StaticJwksClient:
            def get_signing_keys(self, refresh=False):
                if error:
                    raise error
                return keys if keys is not None else [
                    SimpleNamespace(key_id="test-key", key=public_key)
                ]

        client = StaticJwksClient()
        monkeypatch.setattr(auth, "get_jwks_client", lambda: client)
        return client

    return install


@pytest.fixture
def summary_service(monkeypatch):
    service = Mock(
        return_value=main.ResumenResponse(
            summary="Resumen de prueba", main_ideas=["Idea de prueba"]
        )
    )
    monkeypatch.setattr(main, "resumir", service)
    return service


@pytest.fixture
def app_client(summary_service):
    with TestClient(main.app) as client:
        yield client
