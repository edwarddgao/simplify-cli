from __future__ import annotations

import tomllib
from pathlib import Path

from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("simplify-cli"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "page_size": 20,
}


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            return {**DEFAULT_CONFIG, **tomllib.load(f)}
    return dict(DEFAULT_CONFIG)
