from __future__ import annotations

from typing import Any

from simplify_cli.api.client import SimplifyAPIClient
from simplify_cli.api.endpoints import ME, PREFERENCES, RESUMES


def get_profile(client: SimplifyAPIClient) -> dict[str, Any]:
    return client.get(ME)


def get_preferences(client: SimplifyAPIClient) -> dict[str, Any]:
    return client.get(PREFERENCES)


def get_resumes(client: SimplifyAPIClient) -> list[dict[str, Any]]:
    return client.get(RESUMES)
