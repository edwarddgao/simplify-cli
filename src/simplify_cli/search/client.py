from __future__ import annotations

import json as _json
from typing import Any

import httpx

from simplify_cli.api.endpoints import (
    TYPESENSE_API_KEY,
    TYPESENSE_COLLECTION,
    TYPESENSE_SEARCH,
)
from simplify_cli.search.filters import build_filter_by


def _typesense_post(payload: dict[str, Any]) -> dict[str, Any]:
    resp = httpx.post(
        TYPESENSE_SEARCH,
        params={"x-typesense-api-key": TYPESENSE_API_KEY},
        content=_json.dumps(payload),
        headers={"Content-Type": "text/plain"},
        timeout=15.0,
    )
    resp.raise_for_status()
    return resp.json()["results"][0]


def search_jobs(
    *,
    query: str = "*",
    location: str | None = None,
    experience: str | None = None,
    category: str | None = None,
    job_type: str | None = None,
    min_salary: int | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    filter_by = build_filter_by(
        location=location,
        experience=experience,
        category=category,
        job_type=job_type,
        min_salary=min_salary,
    )

    search_params: dict[str, Any] = {
        "q": query,
        "query_by": "title,company_name",
        "sort_by": "updated_date:desc",
        "page": page,
        "per_page": per_page,
    }
    if filter_by:
        search_params["filter_by"] = filter_by

    return _typesense_post({"searches": [{"collection": TYPESENSE_COLLECTION, **search_params}]})


def get_job_by_id(job_id: str) -> dict[str, Any] | None:
    result = _typesense_post({
        "searches": [{
            "collection": TYPESENSE_COLLECTION,
            "q": "*",
            "filter_by": f"id:={job_id}",
            "per_page": 1,
        }]
    })
    hits = result.get("hits", [])
    return hits[0]["document"] if hits else None
