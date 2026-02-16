from __future__ import annotations


def build_filter_by(
    *,
    location: str | None = None,
    experience: str | None = None,
    category: str | None = None,
    job_type: str | None = None,
    min_salary: int | None = None,
) -> str:
    parts: list[str] = []

    if location:
        parts.append(f"locations:=[`{location}`]")
    if experience:
        parts.append(f"experience_level:=[`{experience}`]")
    if category:
        parts.append(f"functions:=[`{category}`]")
    if job_type:
        parts.append(f"type:=[`{job_type}`]")
    if min_salary is not None:
        parts.append(f"max_salary:>={min_salary}")

    return " && ".join(parts) if parts else ""
