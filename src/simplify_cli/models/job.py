from __future__ import annotations

from pydantic import BaseModel, Field

from simplify_cli.models.util import format_salary


class Job(BaseModel):
    id: str = ""
    posting_id: str = ""
    title: str = ""
    company_name: str = ""
    company_id: str = ""
    company_logo: str = ""
    locations: list[str] = Field(default_factory=list)
    experience_level: list[str] = Field(default_factory=list)
    type: str = ""
    functions: list[str] = Field(default_factory=list)
    min_salary: float | None = None
    max_salary: float | None = None
    currency_type: str = ""
    salary_period: int | str | None = None
    sponsors_h1b: bool | str | None = None
    updated_date: int = 0
    start_date: int | str | None = None
    seasons: list[str] = Field(default_factory=list)
    majors: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True, "extra": "ignore"}

    @property
    def location_str(self) -> str:
        return ", ".join(self.locations[:3]) if self.locations else "N/A"

    @property
    def experience_str(self) -> str:
        return ", ".join(self.experience_level) if self.experience_level else ""

    @property
    def salary_str(self) -> str:
        return format_salary(self.min_salary, self.max_salary, self.currency_type)

    @property
    def sponsorship_str(self) -> str:
        if isinstance(self.sponsors_h1b, bool):
            return "Yes" if self.sponsors_h1b else "No"
        return str(self.sponsors_h1b) if self.sponsors_h1b else ""
