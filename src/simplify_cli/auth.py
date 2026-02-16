from __future__ import annotations

import os

import keyring

SERVICE_NAME = "simplify-cli"
CSRF_ACCOUNT = "csrf_token"
AUTH_ACCOUNT = "authorization_token"


def store_tokens(csrf: str, authorization: str) -> None:
    keyring.set_password(SERVICE_NAME, CSRF_ACCOUNT, csrf)
    keyring.set_password(SERVICE_NAME, AUTH_ACCOUNT, authorization)


def get_csrf_token() -> str | None:
    token = os.environ.get("SIMPLIFY_CSRF_TOKEN")
    if token:
        return token
    return keyring.get_password(SERVICE_NAME, CSRF_ACCOUNT)


def get_auth_token() -> str | None:
    token = os.environ.get("SIMPLIFY_AUTH_TOKEN")
    if token:
        return token
    return keyring.get_password(SERVICE_NAME, AUTH_ACCOUNT)


def delete_tokens() -> None:
    for account in (CSRF_ACCOUNT, AUTH_ACCOUNT):
        try:
            keyring.delete_password(SERVICE_NAME, account)
        except keyring.errors.PasswordDeleteError:
            pass


def try_browser_cookies() -> tuple[str, str] | None:
    """Try to extract cookies from Chrome using browser-cookie3.

    Requires browser-cookie3 installed and may trigger a macOS Keychain prompt.
    """
    try:
        import browser_cookie3

        cj = browser_cookie3.chrome(domain_name=".simplify.jobs")
        csrf = auth = None
        for cookie in cj:
            if cookie.name == "csrf":
                csrf = cookie.value
            elif cookie.name == "authorization":
                auth = cookie.value
        if csrf and auth:
            return csrf, auth
    except ImportError:
        pass
    except Exception:
        pass
    return None
