#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from typing import Iterator, Dict
from urllib.parse import urlparse


def add_credentials_to_url(url: str, username: str, password: str) -> str:
    """
    Add username and password to url
    """

    parts = urlparse(url)

    if "@" in parts.netloc:
        netloc = parts.netloc.split("@")[1]
    else:
        netloc = parts.netloc

    return parts.scheme + "://" + username + ":" + password + "@" + netloc + parts.path


def modify_remote(
    repo_path: Path,
    *,
    username: str,
    password: str,
    remote: str = "origin",
):
    """
    modify a remote config to include username and password
    """

    remote_url = (
        subprocess.check_output(
            f"git remote get-url {remote}", cwd=repo_path, shell=True
        )
        .strip()
        .decode()
    )

    if "No such remote" in remote_url:
        print(f"No remote {remote} configured.")
        return None

    new_url = add_credentials_to_url(remote_url, username, password)

    subprocess.check_output(
        f"git remote set-url {remote} {new_url}", cwd=repo_path, shell=True
    )

    print(f"Credentials for {username} added to {repo_path}")


def get_submodule_paths(repo_path: Path) -> Iterator[Path]:
    """
    modify a remote config to include username and password
    """

    submodule_statuses = (
        subprocess.check_output(
            f"git submodule status --recursive", cwd=repo_path, shell=True
        )
        .strip()
        .decode()
        .split("\n")
    )

    submodule_statuses = [x.split(" ") for x in submodule_statuses]

    for sha, path, head in submodule_statuses:
        yield Path(repo_path) / Path(path)


def get_gh_config() -> Dict[str, str]:
    hosts_yml = Path("/root/.config/gh/hosts.yml")
    if hosts_yml.exists() is False:
        raise ValueError("No GH Hosts file")

    # it's small, lets just do it as text to keep requirements down
    with open(hosts_yml, "r") as f:
        rows = f.read().split("\n")

    rows = [[y.strip() for y in x.split(": ")] for x in rows]

    return dict([x for x in rows if len(x) == 2])


def modify_all_submodules():
    config = get_gh_config()
    current = Path(".")
    submodules = list(get_submodule_paths(current))
    for repo in [current] + submodules:
        modify_remote(repo, username=config["user"], password=config["oauth_token"])


if __name__ == "__main__":
    modify_all_submodules()
