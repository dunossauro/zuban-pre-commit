#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["httpx", "tomli", "tomli-w"]
# ///

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import httpx
import tomli
import tomli_w

PYPI_URL = "https://pypi.org/pypi/zuban/json"


def get_latest_zuban_version() -> str:
    resp = httpx.get(PYPI_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()["info"]["version"]


def read_pyproject() -> dict:
    return tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))


def write_pyproject(data: dict) -> None:
    Path("pyproject.toml").write_text(tomli_w.dumps(data), encoding="utf-8")


def update_pyproject_version(new_version: str) -> None:
    data = read_pyproject()
    deps = data["project"]["dependencies"]
    new_deps = [
        re.sub(r"^zuban==.*$", f"zuban=={new_version}", d) if d.startswith("zuban==") else d
        for d in deps
    ]
    data["project"]["dependencies"] = new_deps
    write_pyproject(data)


def update_readme_version(new_version: str) -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    readme = re.sub(r"rev: v[0-9]+\.[0-9]+\.[0-9]+", f"rev: v{new_version}", readme)
    readme = re.sub(r'zuban==[0-9]+\.[0-9]+\.[0-9]+', f"zuban=={new_version}", readme)
    readme = re.sub(r'rev = "v[0-9]+\.[0-9]+\.[0-9]+"', f'rev = "v{new_version}"', readme)
    Path("README.md").write_text(readme, encoding="utf-8")


def git_current_tags() -> set[str]:
    out = subprocess.check_output(["git", "tag"], text=True)
    return set(out.splitlines())


def git_run(*args: str) -> None:
    subprocess.check_call(["git", *args])


def main() -> None:
    latest = get_latest_zuban_version()

    data = read_pyproject()
    current = next(
        d for d in data["project"]["dependencies"] if d.startswith("zuban==")
    ).split("==")[1]

    if latest == current:
        print(f"No update needed (current: {current})")
        return

    tag = f"v{latest}"
    if tag in git_current_tags():
        print(f"Tag {tag} already exists. Nothing to do.")
        return

    print(f"Updating from {current} to {latest}…")

    update_pyproject_version(latest)
    update_readme_version(latest)

    git_run("config", "user.name", "github-actions[bot]")
    git_run("config", "user.email", "github-actions[bot]@users.noreply.github.com")

    git_run("add", "pyproject.toml", "README.md")
    git_run("commit", "-m", f"chore: bump zuban to {latest}")
    git_run("tag", f"v{latest}")
    git_run("push")
    git_run("push", "--tags")

    print(f"Updated and tagged {tag}")


if __name__ == "__main__":
    main()
