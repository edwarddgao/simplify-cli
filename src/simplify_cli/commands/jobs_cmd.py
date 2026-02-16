from __future__ import annotations

import json

import httpx
import typer
from rich import print as rprint
from rich.console import Console

from simplify_cli.display.panels import job_detail_panel
from simplify_cli.display.tables import job_results_table
from simplify_cli.models.job import Job
from simplify_cli.search.client import get_job_by_id, search_jobs

jobs_app = typer.Typer(help="Job search commands")
console = Console()


@jobs_app.command()
def search(
    query: str = typer.Option("*", "-q", "--query", help="Search query"),
    location: str | None = typer.Option(None, "-l", "--location", help="Country filter (e.g. United States)"),
    experience: str | None = typer.Option(None, "-e", "--experience", help="Experience level"),
    category: str | None = typer.Option(None, "-c", "--category", help="Job function/category"),
    job_type: str | None = typer.Option(None, "-t", "--type", help="Job type (Full-Time, Internship, etc.)"),
    min_salary: int | None = typer.Option(None, "-s", "--min-salary", help="Minimum salary"),
    page: int = typer.Option(1, "--page", help="Page number"),
    per_page: int = typer.Option(20, "--per-page", help="Results per page"),
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Search for jobs via Typesense."""
    try:
        with console.status("Searching jobs..."):
            data = search_jobs(
                query=query,
                location=location,
                experience=experience,
                category=category,
                job_type=job_type,
                min_salary=min_salary,
                page=page,
                per_page=per_page,
            )
    except httpx.HTTPStatusError as e:
        rprint(f"[red]Search failed:[/red] {e.response.status_code}")
        raise typer.Exit(1)
    except httpx.ConnectError:
        rprint("[red]Error:[/red] Could not connect to search service.")
        raise typer.Exit(1)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    hits = data.get("hits", [])
    found = data.get("found", 0)

    if not hits:
        rprint("[yellow]No jobs found matching your criteria.[/yellow]")
        return

    jobs = [Job.model_validate(hit["document"]) for hit in hits]
    table = job_results_table(jobs, page=page, total=found)
    console.print(table)
    total_pages = (found + per_page - 1) // per_page
    rprint(f"[dim]Page {page}/{total_pages} ({found} total results)[/dim]")


@jobs_app.command()
def view(
    job_id: str = typer.Argument(help="Job ID to view details"),
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """View details for a specific job."""
    try:
        with console.status("Fetching job details..."):
            doc = get_job_by_id(job_id)
    except httpx.HTTPStatusError as e:
        rprint(f"[red]Lookup failed:[/red] {e.response.status_code}")
        raise typer.Exit(1)
    except httpx.ConnectError:
        rprint("[red]Error:[/red] Could not connect to search service.")
        raise typer.Exit(1)

    if not doc:
        rprint(f"[red]Job {job_id} not found.[/red]")
        raise typer.Exit(1)

    if output_json:
        print(json.dumps(doc, indent=2))
        return

    job = Job.model_validate(doc)
    console.print(job_detail_panel(job))
