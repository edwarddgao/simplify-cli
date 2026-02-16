from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

import httpx
from rich import print as rprint

from simplify_cli.auth import get_auth_token, get_csrf_token


class SimplifyAPIClient:
    def __init__(self) -> None:
        csrf = get_csrf_token()
        auth = get_auth_token()
        if not csrf or not auth:
            rprint("[red]Error:[/red] Not authenticated. Run [bold]simplify auth login[/bold] first.")
            sys.exit(1)
        self._client = httpx.Client(
            headers={
                "X-CSRF-TOKEN": csrf,
                "Content-Type": "application/json",
            },
            cookies={"csrf": csrf, "authorization": auth},
            timeout=30.0,
            follow_redirects=True,
        )

    def __enter__(self) -> SimplifyAPIClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._client.close()

    def get(self, url: str, **params: Any) -> Any:
        resp = self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, url: str, json: Any = None) -> Any:
        resp = self._client.post(url, json=json)
        resp.raise_for_status()
        return resp.json()

    def get_raw(self, url: str, **params: Any) -> httpx.Response:
        resp = self._client.get(url, params=params)
        resp.raise_for_status()
        return resp
