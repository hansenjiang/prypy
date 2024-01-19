"""Read Python scripts and identify objects.
"""


# Imports


from pathlib import Path
from typing import Union

from . import models, utils


# Constants

# TODO remove me for cli
MORSE_PATH = Path(".").resolve()


# Functions


def read_modules(package_path: Path) -> list[models.Module]:
    pass


def read_package(package_path: Path) -> models.Package:
    # Create and return package object by calling module and subpackage creation
    package = models.Package(package_path.name, read_modules(package_path), subpackages)
    return package


def gen_package_dict(package_path: Path) -> dict[str, Union[models.Package, dict]]:
    package_dict = {}
    items = utils.get_item_names(package_path)


def read_repository(repo_path: Path) -> models.Repository:
    # TODO implement find first package function instead of this
    # Terminate if ``src/package_name`` directory is not in repository
    items = utils.get_item_names(repo_path)
    if ("src" not in items) or (items["src"]):
        raise ImportError(f"No `src` directory found in repository {repo_path.name}.")
    src_items = utils.get_item_names(repo_path / "src")
    package_name = "_".join(repo_path.name.split("-"))
    if (package_name not in src_items) or (src_items[package_name]):
        raise ImportError(f"No `{package_name}` package found in {repo_path / 'src'}.")

    # Read source package (and consequently, subpackages)
    source = read_package
    # TODO finish

    # Create and return repository object by calling package creation
    repository = models.Repository(
        package_name, read_package(repo_path / "src" / "package_name"), repo_path
    )
    return repository
