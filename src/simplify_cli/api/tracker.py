from __future__ import annotations

from typing import Any

from simplify_cli.api.client import SimplifyAPIClient
from simplify_cli.api.endpoints import (
    TRACKER,
    TRACKER_APPLIED,
    TRACKER_EXPORT_CSV,
    TRACKER_SANKEY,
    TRACKER_SAVE,
    TRACKER_STATUS_UPDATE,
)


def list_tracker(client: SimplifyAPIClient, page: int = 1, size: int = 20, status: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"page": page, "size": size}
    if status:
        params["status"] = status
    return client.get(TRACKER, **params)


def save_job(client: SimplifyAPIClient, job_posting_id: str) -> dict[str, Any]:
    return client.post(TRACKER_SAVE, json={"job_posting_id": job_posting_id})


def mark_applied(client: SimplifyAPIClient, job_posting_id: str) -> dict[str, Any]:
    return client.post(TRACKER_APPLIED, json={"job_posting_id": job_posting_id})


def update_status(client: SimplifyAPIClient, tracker_id: str, status: str) -> dict[str, Any]:
    return client.post(TRACKER_STATUS_UPDATE, json={"id": tracker_id, "status": status})


def export_csv(client: SimplifyAPIClient) -> bytes:
    resp = client.get_raw(TRACKER_EXPORT_CSV)
    return resp.content


def get_stats(client: SimplifyAPIClient) -> dict[str, Any]:
    return client.get(TRACKER_SANKEY)
