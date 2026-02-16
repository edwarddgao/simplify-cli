from __future__ import annotations

import json
from pathlib import Path

import httpx
import typer
from rich import print as rprint
from rich.console import Console

from simplify_cli.api.client import SimplifyAPIClient
from simplify_cli.api.tracker import (
    export_csv,
    get_stats,
    list_tracker,
    mark_applied,
    save_job,
    update_status,
)
from simplify_cli.display.tables import tracker_table
from simplify_cli.models.tracker import TrackerPage, TrackerStatus

tracker_app = typer.Typer(help="Application tracker commands")
console = Console()


def _handle_api_error(e: httpx.HTTPStatusError) -> None:
    if e.response.status_code == 401:
        rprint("[red]Error:[/red] Session expired. Run [bold]simplify auth login[/bold]")
    else:
        rprint(f"[red]API error:[/red] {e.response.status_code}")
    raise typer.Exit(1)


@tracker_app.command("list")
def list_cmd(
    status: str | None = typer.Option(None, "-s", "--status", help="Filter by status"),
    page: int = typer.Option(1, "-p", "--page", help="Page number"),
    size: int = typer.Option(20, "--size", help="Items per page"),
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """List tracked jobs."""
    try:
        with SimplifyAPIClient() as client:
            data = list_tracker(client, page=page, size=size, status=status)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    tp = TrackerPage.model_validate(data)
    if not tp.items:
        rprint("[yellow]No tracked jobs found.[/yellow]")
        return

    table = tracker_table(tp.items, page=tp.page, total=tp.total)
    console.print(table)
    rprint(f"[dim]Page {tp.page}/{tp.pages}[/dim]")


@tracker_app.command()
def save(
    job_id: str = typer.Argument(help="Job posting ID to save"),
) -> None:
    """Save a job to your tracker."""
    try:
        with SimplifyAPIClient() as client:
            save_job(client, job_id)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)
    rprint(f"[green]Job {job_id[:8]}… saved to tracker.[/green]")


@tracker_app.command()
def applied(
    job_id: str = typer.Argument(help="Job posting ID to mark as applied"),
) -> None:
    """Mark a job as applied."""
    try:
        with SimplifyAPIClient() as client:
            mark_applied(client, job_id)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)
    rprint(f"[green]Job {job_id[:8]}… marked as applied.[/green]")


@tracker_app.command()
def status_update(
    tracker_id: str = typer.Argument(help="Tracker item ID"),
    new_status: TrackerStatus = typer.Argument(help="New status"),
) -> None:
    """Update the status of a tracked job."""
    try:
        with SimplifyAPIClient() as client:
            update_status(client, tracker_id, new_status.value)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)
    rprint(f"[green]Status updated to {new_status.value}.[/green]")


@tracker_app.command()
def export(
    output: Path = typer.Option("tracker.csv", "-o", "--output", help="Output CSV file"),
) -> None:
    """Export tracker to CSV."""
    try:
        with SimplifyAPIClient() as client:
            csv_bytes = export_csv(client)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)
    output.write_bytes(csv_bytes)
    rprint(f"[green]Exported tracker to {output}[/green]")


@tracker_app.command()
def stats(
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Show tracker statistics."""
    try:
        with SimplifyAPIClient() as client:
            data = get_stats(client)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    # Extract statistics from sankey data
    stats_data = None
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "debug_info" in item:
                stats_data = item["debug_info"].get("statistics", {})
                break

    if not stats_data:
        rprint("[yellow]No statistics available.[/yellow]")
        return

    rprint("[bold]Tracker Statistics[/bold]\n")

    counts = stats_data.get("stage_conversion_rates", {}).get("counts", {})
    if counts:
        rprint(f"  Applications:  [bold]{counts.get('applications', 0)}[/bold]")
        rprint(f"  Screenings:    [bold]{counts.get('screenings', 0)}[/bold]")
        rprint(f"  Interviews:    [bold]{counts.get('interviews', 0)}[/bold]")
        rprint(f"  Offers:        [bold]{counts.get('offers', 0)}[/bold]")
        rprint()

    ghost = stats_data.get("ghost_rate_percent")
    if ghost is not None:
        rprint(f"  Ghost rate:    [bold]{ghost}%[/bold]")
    avg_days = stats_data.get("average_days_to_first_response")
    if avg_days is not None:
        rprint(f"  Avg response:  [bold]{avg_days} days[/bold]")

    avg_apps = stats_data.get("average_applications", {})
    if avg_apps:
        rprint(f"\n  Apps/week:     [bold]{avg_apps.get('weekly', 0)}[/bold]")
        rprint(f"  Apps/month:    [bold]{avg_apps.get('monthly', 0)}[/bold]")
        rprint(f"  Active weeks:  [bold]{stats_data.get('active_weeks', 0)}[/bold]")

    busiest = stats_data.get("most_active_weekday", {})
    if busiest:
        rprint(f"  Busiest day:   [bold]{busiest.get('name', '')}[/bold] ({busiest.get('applications', 0)} apps)")
