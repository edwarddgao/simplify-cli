from __future__ import annotations

from datetime import datetime, timezone

from rich.table import Table

from simplify_cli.models.job import Job
from simplify_cli.models.tracker import TrackerItem


def job_results_table(jobs: list[Job], page: int = 1, total: int = 0) -> Table:
    table = Table(
        title=f"Job Results (page {page}, {total} total)",
        show_lines=True,
    )
    table.add_column("ID", style="dim", max_width=10)
    table.add_column("Title", style="bold cyan", max_width=35)
    table.add_column("Company", style="green", max_width=20)
    table.add_column("Location", max_width=25)
    table.add_column("Type", max_width=12)
    table.add_column("Salary", max_width=20)

    for job in jobs:
        table.add_row(
            job.id[:8] if len(job.id) > 8 else job.id,
            job.title,
            job.company_name,
            job.location_str,
            job.type,
            job.salary_str,
        )
    return table


def tracker_table(items: list[TrackerItem], page: int = 1, total: int = 0) -> Table:
    table = Table(
        title=f"Tracker (page {page}, {total} total)",
        show_lines=True,
    )
    table.add_column("ID", style="dim", max_width=10)
    table.add_column("Title", style="bold cyan", max_width=30)
    table.add_column("Company", style="green", max_width=20)
    table.add_column("Status", max_width=14)
    table.add_column("Location", max_width=20)
    table.add_column("Saved", max_width=12)

    status_colors = {
        "saved": "yellow",
        "applied": "blue",
        "interviewing": "magenta",
        "offer": "green",
        "rejected": "red",
        "withdrawn": "dim",
    }

    for item in items:
        status = item.current_status
        color = status_colors.get(status.lower(), "white")
        saved = _format_date(item.tracked_date)
        table.add_row(
            item.id[:8] if len(item.id) > 8 else item.id,
            item.job_posting_title,
            item.company_name,
            f"[{color}]{status}[/{color}]",
            item.job_posting_location,
            saved,
        )
    return table


def _format_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return date_str[:10]
