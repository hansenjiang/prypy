"""Various utility functions for the package.
"""


# Imports


from pathlib import Path


# Functions


def get_item_names(path: Path) -> dict[str, bool]:
    """Get dict of items contained in passed directory path.

    Parameters
    ----------
    path : Path
        Path to directory to be inspected.

    Returns
    -------
    dict[str, bool]
        Items indexed by name, containing bool evaluating whether or not they
        are files.
    """
    return {item.name: item.is_file() for item in path.iterdir()}


def get_item_paths(path: Path) -> list[Path]:
    """Get paths to items contained in passed directory path.

    Parameters
    ----------
    path : Path
        Path to directory to be inspected.

    Returns
    -------
    list[Path]
        List of paths to items within directory.
    """
    return list(path.iterdir())
