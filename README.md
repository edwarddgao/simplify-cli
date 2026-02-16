# simplify-cli

A CLI for [Simplify.jobs](https://simplify.jobs) — browse jobs, manage your application tracker, and view your profile from the terminal.

## Install

```bash
pip install -e .
```

Requires Python 3.11+.

## Authentication

```bash
# Auto-extract cookies from Chrome (recommended)
simplify auth login

# Or paste cookies manually from DevTools
simplify auth login --manual

# Check status
simplify auth status

# Log out
simplify auth logout
```

Auto-extract reads your Chrome cookies via `browser-cookie3` and may prompt for Keychain access on macOS. For manual mode, copy the `csrf` and `authorization` cookie values from DevTools → Application → Cookies → simplify.jobs.

## Job Search

Search jobs without authentication — powered by Typesense.

```bash
# Basic search
simplify jobs search -q "software engineer"

# With filters
simplify jobs search -q "backend" -t "Full-Time" -e "Entry Level/New Grad" -s 100000

# View job details
simplify jobs view <job-id>

# JSON output for scripting
simplify jobs search -q "data scientist" --json | jq '.hits[].document.title'
```

**Options:**
| Flag | Description |
|------|-------------|
| `-q` / `--query` | Search text (default: `*`) |
| `-l` / `--location` | Location filter |
| `-e` / `--experience` | Experience level |
| `-c` / `--category` | Job function/category |
| `-t` / `--type` | Job type (Full-Time, Internship, etc.) |
| `-s` / `--min-salary` | Minimum salary |
| `--page` | Page number |
| `--per-page` | Results per page |
| `--json` | JSON output |

## Tracker

Manage your Simplify application tracker (requires auth).

```bash
# List tracked jobs
simplify tracker list
simplify tracker list -s applied --size 10

# Save a job / mark as applied
simplify tracker save <job-id>
simplify tracker applied <job-id>

# Update status
simplify tracker status-update <tracker-id> interviewing

# Export to CSV
simplify tracker export -o applications.csv

# View statistics
simplify tracker stats
```

## Profile

```bash
simplify profile show          # Education, experience, links
simplify profile preferences   # Job preferences, skills, locations
simplify profile resumes       # List uploaded resumes
```

All commands support `--json` for machine-readable output.

## Tech Stack

- [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) for the CLI
- [httpx](https://www.python-httpx.org/) for HTTP
- [Pydantic](https://docs.pydantic.dev/) for data models
- [keyring](https://pypi.org/project/keyring/) for secure credential storage
