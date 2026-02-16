from __future__ import annotations

from datetime import datetime, timezone

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from simplify_cli.models.job import Job
from simplify_cli.models.profile import Education, Experience, Profile, Resume


def job_detail_panel(job: Job) -> Panel:
    lines = Text()
    lines.append(f"{job.title}\n", style="bold cyan")
    lines.append(f"{job.company_name}\n", style="bold green")
    lines.append("\n")
    lines.append("Location: ", style="bold")
    lines.append(f"{job.location_str}\n")
    lines.append("Type: ", style="bold")
    lines.append(f"{job.type}\n")
    if job.experience_str:
        lines.append("Experience: ", style="bold")
        lines.append(f"{job.experience_str}\n")
    if job.salary_str:
        lines.append("Salary: ", style="bold")
        lines.append(f"{job.salary_str}\n")
    if job.functions:
        lines.append("Functions: ", style="bold")
        lines.append(f"{', '.join(job.functions)}\n")
    if job.sponsorship_str:
        lines.append("H1B Sponsorship: ", style="bold")
        lines.append(f"{job.sponsorship_str}\n")
    if job.start_date:
        start = str(job.start_date)
        if isinstance(job.start_date, int):
            try:
                start = datetime.fromtimestamp(job.start_date, tz=timezone.utc).strftime("%Y-%m-%d")
            except (ValueError, OSError):
                pass
        lines.append("Start Date: ", style="bold")
        lines.append(f"{start}\n")

    updated = ""
    if job.updated_date:
        try:
            dt = datetime.fromtimestamp(job.updated_date, tz=timezone.utc)
            updated = dt.strftime("%Y-%m-%d")
        except (ValueError, OSError):
            pass
    if updated:
        lines.append("Updated: ", style="bold")
        lines.append(f"{updated}\n")

    lines.append("\nID: ", style="bold")
    lines.append(f"{job.id}\n", style="dim")

    return Panel(lines, title="Job Details", border_style="blue")


def profile_panel(profile: Profile) -> Panel:
    lines = Text()
    lines.append(f"{profile.full_name}\n", style="bold cyan")
    if profile.email:
        lines.append(f"{profile.email}\n", style="dim")
    if profile.phone:
        lines.append(f"{profile.phone}\n")
    if profile.location:
        lines.append(f"{profile.location}\n")
    lines.append("\n")
    if profile.linkedin:
        lines.append("LinkedIn: ", style="bold")
        lines.append(f"{profile.linkedin}\n", style="underline blue")
    if profile.github:
        lines.append("GitHub: ", style="bold")
        lines.append(f"{profile.github}\n", style="underline blue")
    if profile.website:
        lines.append("Website: ", style="bold")
        lines.append(f"{profile.website}\n", style="underline blue")
    if profile.skills:
        lines.append("\nSkills: ", style="bold")
        lines.append(f"{', '.join(profile.skills)}\n")
    return Panel(lines, title="Profile", border_style="green")


def education_table(education: list[Education]) -> Table:
    table = Table(title="Education", show_lines=True)
    table.add_column("School", style="bold")
    table.add_column("Degree")
    table.add_column("GPA")
    table.add_column("Dates", style="dim")
    for edu in education:
        gpa = f"{edu.gpa:.1f}" if edu.gpa else ""
        table.add_row(edu.school_name, edu.degree_str, gpa, edu.dates_str)
    return table


def experience_table(experience: list[Experience]) -> Table:
    table = Table(title="Experience", show_lines=True)
    table.add_column("Company", style="bold")
    table.add_column("Title")
    table.add_column("Location")
    table.add_column("Dates", style="dim")
    for exp in experience:
        table.add_row(exp.company_name, exp.title, exp.location, exp.dates_str)
    return table


def preferences_panel(raw_data: dict) -> Panel:
    lines = Text()

    # Regions
    regions = raw_data.get("region", [])
    if regions:
        lines.append("Locations: ", style="bold")
        lines.append(f"{', '.join(r.get('name', '') for r in regions)}\n")

    # Functions
    funcs = raw_data.get("function", [])
    if funcs:
        lines.append("Roles: ", style="bold")
        lines.append(f"{', '.join(f.get('title', '') for f in funcs)}\n")

    # Industries
    industries = raw_data.get("industry", [])
    if industries:
        lines.append("Industries: ", style="bold")
        lines.append(f"{', '.join(i.get('name', '') for i in industries[:10])}")
        if len(industries) > 10:
            lines.append(f" (+{len(industries) - 10} more)")
        lines.append("\n")

    # Experience levels
    levels = []
    for key, label in [("prefers_intern", "Intern"), ("prefers_entry", "Entry"), ("prefers_junior", "Junior"),
                        ("prefers_mid", "Mid"), ("prefers_senior", "Senior"), ("prefers_staff", "Staff")]:
        if raw_data.get(key):
            levels.append(label)
    if levels:
        lines.append("Experience: ", style="bold")
        lines.append(f"{', '.join(levels)}\n")

    # Skills
    skills = raw_data.get("skill", [])
    if skills:
        lines.append("Skills: ", style="bold")
        names = [s.get("skill", {}).get("name", "") for s in skills[:15]]
        lines.append(f"{', '.join(n for n in names if n)}")
        if len(skills) > 15:
            lines.append(f" (+{len(skills) - 15} more)")
        lines.append("\n")

    # Work auth
    auths = []
    if raw_data.get("work_auth_us"):
        auths.append("US")
    if raw_data.get("work_auth_ca"):
        auths.append("Canada")
    if raw_data.get("work_auth_uk"):
        auths.append("UK")
    if auths:
        lines.append("Work Auth: ", style="bold")
        lines.append(f"{', '.join(auths)}\n")

    # Min salary
    salary = raw_data.get("prefers_salary")
    if salary:
        lines.append("Min Salary: ", style="bold")
        lines.append(f"${salary:,}k\n")

    if not lines.plain.strip():
        lines.append("No preferences set.\n")

    return Panel(lines, title="Job Preferences", border_style="yellow")


def resumes_table(resumes: list[Resume]) -> Table:
    table = Table(title="Resumes", show_lines=True)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Created")
    table.add_column("Default")
    for r in resumes:
        default = "[green]Yes[/green]" if r.default else "No"
        created = r.date_generated[:10] if r.date_generated else ""
        table.add_row(r.id[:8], r.name, created, default)
    return table
