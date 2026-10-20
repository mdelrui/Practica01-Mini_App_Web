import math
import os
from functools import lru_cache

import jwt
from jwt import PyJWK, PyJWKClient
from jwt.exceptions import (
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
    PyJWKError,
    PyJWKSetError,
)


class InvalidSessionToken(Exception):
    pass


class SessionVerifierUnavailable(Exception):
    pass


@lru_cache(maxsize=8)
def _create_jwks_client(jwks_url: str, timeout: float) -> PyJWKClient:
    return PyJWKClient(jwks_url, timeout=timeout)


def get_jwks_client() -> PyJWKClient:
    jwks_url = os.getenv("CLERK_JWKS_URL", "").strip()
    timeout_value = os.getenv("CLERK_JWKS_TIMEOUT", "").strip()

    if not jwks_url or not timeout_value:
        raise SessionVerifierUnavailable("Clerk JWKS configuration is incomplete")

    try:
        timeout = float(timeout_value)
    except ValueError as exc:
        raise SessionVerifierUnavailable("Clerk JWKS timeout is invalid") from exc

    if not math.isfinite(timeout) or timeout <= 0:
        raise SessionVerifierUnavailable(
            "Clerk JWKS timeout must be finite and positive"
        )

    return _create_jwks_client(jwks_url, timeout)


def _get_signing_key(client: PyJWKClient, kid: str) -> PyJWK:
    try:
        keys = client.get_signing_keys()
        key = next((candidate for candidate in keys if candidate.key_id == kid), None)
        if key is None:
            keys = client.get_signing_keys(refresh=True)
            key = next((candidate for candidate in keys if candidate.key_id == kid), None)
    except (
        PyJWKClientConnectionError,
        PyJWKClientError,
        PyJWKError,
        PyJWKSetError,
    ) as exc:
        raise SessionVerifierUnavailable("Clerk JWKS could not be used") from exc

    if key is None:
        raise InvalidSessionToken("No Clerk signing key matches the token")
    return key


def verify_session_token(token: str) -> None:
    issuer = os.getenv("CLERK_ISSUER", "").strip()
    if not issuer:
        raise SessionVerifierUnavailable("Clerk issuer is not configured")

    try:
        header = jwt.get_unverified_header(token)
    except InvalidTokenError as exc:
        raise InvalidSessionToken("Malformed session token") from exc

    kid = header.get("kid")
    if header.get("alg") != "RS256" or not isinstance(kid, str) or not kid:
        raise InvalidSessionToken("Unsupported session token header")

    signing_key = _get_signing_key(get_jwks_client(), kid)

    try:
        jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=issuer,
            options={"require": ["exp"]},
        )
    except InvalidTokenError as exc:
        raise InvalidSessionToken("Session token was rejected") from exc
