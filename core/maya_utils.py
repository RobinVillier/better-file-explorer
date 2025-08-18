import os

from BetterFileExplorer.core import load


def build_path(environment: dict, role: str) -> str:
    """ Returns a path depending on the environment and the role that is passed """
    base_path = load.get_project_path()

    if role == "client":
        return base_path

    elif role == "project":
        return os.path.join(base_path, environment.get("client", ""))

    elif role == "asset":
        return os.path.join(base_path, environment.get("client", ""), environment.get("project", ""), "Assets")

    elif role == "task":
        return os.path.join(base_path,
                            environment.get("client", ""),
                            environment.get("project", ""),
                            "Assets",
                            environment.get("asset", ""),
                            "maya",
                            "scenes")

    elif role == "data":
        return os.path.join(base_path,
                            environment.get("client", ""),
                            environment.get("project", ""),
                            "Assets",
                            environment.get("asset", ""),
                            "maya",
                            "data")

    return base_path
