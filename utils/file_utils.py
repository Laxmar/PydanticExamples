import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


def load_json(file_path: Path | str) -> Any:
	with open(file_path, "r") as f:
		return json.load(f)


def save_json(data: object, file_path: Path | str) -> None:
	with open(file_path, "w") as f:
		json.dump(data, f, indent=4)


def load_yaml(file_path: Path | str) -> Any:
	with open(file_path, "r") as f:
		return yaml.safe_load(f)


def save_yaml(data: object, file_path: Path | str) -> None:
	with open(file_path, "w") as f:
		yaml.dump(data, f, default_flow_style=False)


def get_git_revision_hash() -> str:
	return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
