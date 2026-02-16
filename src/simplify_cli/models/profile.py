from __future__ import annotations

from pydantic import BaseModel, Field


class NestedName(BaseModel):
    name: str = ""
    model_config = {"extra": "ignore"}


class Education(BaseModel):
    education: NestedName | None = None
    major_custom_name: str | None = None
    degree: int | str | None = None
    gpa: float | None = None
    start_month: int | None = None
    start_year: int | None = None
    grad_month: int | None = None
    grad_year: int | None = None

    model_config = {"extra": "ignore"}

    @property
    def school_name(self) -> str:
        return self.education.name if self.education else ""

    @property
    def degree_str(self) -> str:
        if self.degree is None:
            return ""
        degree_map = {1: "Bachelor's", 2: "Master's", 3: "PhD", 4: "Associate's", 5: "Other"}
        if isinstance(self.degree, int):
            return degree_map.get(self.degree, str(self.degree))
        return str(self.degree)

    @property
    def dates_str(self) -> str:
        start = f"{self.start_month}/{self.start_year}" if self.start_month and self.start_year else ""
        end = f"{self.grad_month}/{self.grad_year}" if self.grad_month and self.grad_year else ""
        if start and end:
            return f"{start} – {end}"
        return start or end


class Experience(BaseModel):
    company: NestedName | None = None
    title: str = ""
    location: str = ""
    start_month: int | None = None
    start_year: int | None = None
    end_month: int | None = None
    end_year: int | None = None
    currently_working: bool = False

    model_config = {"extra": "ignore"}

    @property
    def company_name(self) -> str:
        return self.company.name if self.company else ""

    @property
    def dates_str(self) -> str:
        start = f"{self.start_month}/{self.start_year}" if self.start_month and self.start_year else ""
        end = "Present" if self.currently_working else (
            f"{self.end_month}/{self.end_year}" if self.end_month and self.end_year else ""
        )
        if start and end:
            return f"{start} – {end}"
        return start or end


class Profile(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)

    model_config = {"extra": "ignore"}

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class Resume(BaseModel):
    id: str = ""
    name: str = ""
    file_name: str = ""
    date_generated: str = ""
    date_last_edited: str = ""
    default: bool = False

    model_config = {"extra": "ignore"}
