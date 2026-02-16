import typer

from simplify_cli.commands.auth_cmd import auth_app
from simplify_cli.commands.jobs_cmd import jobs_app
from simplify_cli.commands.profile_cmd import profile_app
from simplify_cli.commands.tracker_cmd import tracker_app

app = typer.Typer(
    name="simplify",
    help="CLI for Simplify.jobs — browse jobs, manage tracker, view profile.",
    no_args_is_help=True,
    pretty_exceptions_short=True,
)

app.add_typer(auth_app, name="auth")
app.add_typer(jobs_app, name="jobs")
app.add_typer(tracker_app, name="tracker")
app.add_typer(profile_app, name="profile")
