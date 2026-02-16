from __future__ import annotations

import typer
from rich import print as rprint

from simplify_cli.auth import (
    delete_tokens,
    get_auth_token,
    get_csrf_token,
    store_tokens,
    try_browser_cookies,
)

auth_app = typer.Typer(help="Authentication commands")


@auth_app.command()
def login(
    manual: bool = typer.Option(False, "--manual", help="Manually paste cookies instead of auto-extracting"),
) -> None:
    """Log in by extracting cookies from Chrome, or paste them manually."""
    if not manual:
        rprint("[dim]Attempting to extract cookies from Chrome...[/dim]")
        result = try_browser_cookies()
        if result:
            csrf, auth = result
            store_tokens(csrf, auth)
            rprint("[green]Cookies extracted and stored successfully.[/green]")
            _verify_login()
            return
        else:
            rprint("[yellow]Could not auto-extract cookies from Chrome.[/yellow]")
            rprint("[dim]Falling back to manual mode. You can also try closing Chrome first.[/dim]\n")

    rprint(
        "[bold]To get your cookies:[/bold]\n"
        "1. Log in to [link=https://simplify.jobs]simplify.jobs[/link]\n"
        "2. Open DevTools (F12) → Application → Cookies → simplify.jobs\n"
        "3. Copy the values of both [bold]csrf[/bold] and [bold]authorization[/bold] cookies\n"
    )
    csrf = typer.prompt("Paste your csrf cookie").strip()
    auth = typer.prompt("Paste your authorization cookie").strip()

    if not csrf or not auth:
        rprint("[red]Both cookies are required.[/red]")
        raise typer.Exit(1)

    store_tokens(csrf, auth)
    rprint("[green]Tokens stored successfully.[/green]")
    _verify_login()


@auth_app.command()
def logout() -> None:
    """Clear stored credentials."""
    delete_tokens()
    rprint("[green]Logged out. Credentials removed.[/green]")


@auth_app.command()
def status() -> None:
    """Show current authentication status."""
    csrf = get_csrf_token()
    auth = get_auth_token()
    if not csrf or not auth:
        rprint("[yellow]Not authenticated.[/yellow] Run [bold]simplify auth login[/bold]")
        raise typer.Exit(1)
    _verify_login()


def _verify_login() -> None:
    """Try to fetch profile to verify credentials."""
    try:
        from simplify_cli.api.client import SimplifyAPIClient
        from simplify_cli.api.endpoints import ME

        with SimplifyAPIClient() as client:
            data = client.get(ME)
        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        email = data.get("email", "")
        rprint(f"[green]Authenticated[/green] as [bold]{name}[/bold] ({email})")
    except SystemExit:
        raise
    except Exception as e:
        rprint(f"[yellow]Credentials found but could not verify: {e}[/yellow]")
