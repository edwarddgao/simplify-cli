from __future__ import annotations

import json

import httpx
import typer
from rich import print as rprint
from rich.console import Console

from simplify_cli.api.client import SimplifyAPIClient
from simplify_cli.api.profile import get_preferences, get_profile, get_resumes
from simplify_cli.display.panels import (
    education_table,
    experience_table,
    preferences_panel,
    profile_panel,
    resumes_table,
)
from simplify_cli.models.profile import Profile, Resume

profile_app = typer.Typer(help="Profile commands")
console = Console()


def _handle_api_error(e: httpx.HTTPStatusError) -> None:
    if e.response.status_code == 401:
        rprint("[red]Error:[/red] Session expired. Run [bold]simplify auth login[/bold]")
    else:
        rprint(f"[red]API error:[/red] {e.response.status_code}")
    raise typer.Exit(1)


@profile_app.command()
def show(
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Display your profile."""
    try:
        with SimplifyAPIClient() as client:
            data = get_profile(client)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    profile = Profile.model_validate(data)
    console.print(profile_panel(profile))
    if profile.education:
        console.print(education_table(profile.education))
    if profile.experience:
        console.print(experience_table(profile.experience))


@profile_app.command()
def preferences(
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Show your job preferences."""
    try:
        with SimplifyAPIClient() as client:
            data = get_preferences(client)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    console.print(preferences_panel(data))


@profile_app.command()
def resumes(
    output_json: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """List your resumes."""
    try:
        with SimplifyAPIClient() as client:
            data = get_resumes(client)
    except httpx.HTTPStatusError as e:
        _handle_api_error(e)

    if output_json:
        print(json.dumps(data, indent=2))
        return

    items = data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    if not items:
        rprint("[yellow]No resumes found.[/yellow]")
        return

    resume_list = [Resume.model_validate(r) for r in items]
    console.print(resumes_table(resume_list))
