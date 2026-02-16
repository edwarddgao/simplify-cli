from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from simplify_cli.models.util import format_salary

STATUS_MAP = {
    1: "Saved",
    2: "Applied",
    3: "Interviewing",
    4: "Offer",
    5: "Rejected",
    6: "Withdrawn",
}


class TrackerStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class TrackerCompany(BaseModel):
    name: str = ""
    model_config = {"extra": "ignore"}


class StatusEvent(BaseModel):
    status: int = 0
    timestamp: str = ""
    model_config = {"extra": "ignore"}


class TrackerItem(BaseModel):
    id: str = ""
    job_posting_id: str | None = None
    job_posting_title: str = ""
    job_posting_location: str = ""
    job_posting_url: str = ""
    company_id: str = ""
    company: TrackerCompany | None = None
    tracked_date: str = ""
    status_events: list[StatusEvent] = Field(default_factory=list)
    salary_low: float | None = None
    salary_high: float | None = None
    currency_type: str = ""
    favorite: bool = False

    model_config = {"extra": "ignore"}

    @property
    def company_name(self) -> str:
        return self.company.name if self.company else ""

    @property
    def current_status(self) -> str:
        if not self.status_events:
            return ""
        latest = max(self.status_events, key=lambda e: e.timestamp)
        return STATUS_MAP.get(latest.status, str(latest.status))

    @property
    def salary_str(self) -> str:
        return format_salary(self.salary_low, self.salary_high, self.currency_type)


class TrackerPage(BaseModel):
    total: int = 0
    items: list[TrackerItem] = Field(default_factory=list)
    page: int = 1
    size: int = 20
    pages: int = 1

    model_config = {"extra": "ignore"}
