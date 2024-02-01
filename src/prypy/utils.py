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


def tab_level(line: str) -> int:
    """Return the tab level of the current line.

    Parameters
    ----------
    line : str
        Module line to be inspected.

    Returns
    -------
    int
        Number of indents to beginning of line content.
    """
    return max(len(line.split("\t")), len(line.split("    "))) - 1


def is_encased(
    line: str | list[str], pivot: str, left: str, right: str | None = None
) -> list[bool]:
    # Set right to left if not declared
    if right is None:
        right = left

    # Set line to single line if multiple
    if isinstance(line, list):
        line = "".join(line)

    # Raise error if `pivot` not in `line`
    if pivot not in line:
        raise ValueError(f"`{pivot}` not found in line `{line}`.")

    # Create open/close status and pivot tracker
    met = [[False, False] for i in range(len(line.split(pivot)) - 1)]
    n_pivot = 0

    # Read line from left to right
    i = 0
    while i < len(line):
        if (i + len(pivot) - 1 < len(line)) and (line[i : i + len(pivot)] == pivot):
            n_pivot += 1
            if met[left]:
                pass

        if i + len(left) - 1 < len(line):
            pass

    # Check multiple lines
    if isinstance(line, list):
        pass
    # Check single line
    else:
        #
        segments = line.split(pivot)
        i = 0
        while i < len(segments) - 1:
            # Not encased if `left` doesn't appear before `pivot`
            if left not in segments[i]:
                encased.append(False)
            else:
                pass
            i += 1


def remove_comments(lines: list[str]) -> list[str]:
    # Iterate over all lines
    i = 0
    while i < len(lines):
        # Remove single line comments
        if "#" in lines[i]:
            # Check each instance of "#"
            j = 0
            while j < len(lines[i].split("#")) - 1:
                if lines[j][-1] == '"':
                    pass
                j += 1

    # Skip empty lines and comments
    if (len(line.strip()) == 0) or (line.strip()[0] == "#"):
        i += 1
        continue
    # Skip multi-line strings
    elif '"""' in line:
        # If line is variable declaration, store if module-level constant
        if (
            ("=" in line.split('"""')[0])
            and (line.split('"""')[0].split("=")[0].strip().isupper())
            and (utils.tab_level(line) == 0)
        ):
            constant_name = line.split('"""')[0].split("=")[0].strip()
            constant_str = line.split('"""')[1].strip()

            # If only opening quotation mark is found, find closing mark
            if len(line.split('"""')) == 2:
                i += 1
                line = lines[i]
                while ('"""' not in line) and (i < len(lines)):
                    constant_str += "\n" + line.strip()
                    i += 1
                    line = lines[i]
                if len(line.split('"""')[0].strip()) > 0:
                    constant_str += "\n" + line.strip()

            # Create and store constant
            module.constants.append(Variable(constant_name, str, constant_str, module))

        # Otherwise skip string
        else:
            # If only opening quotation mark is found, find closing mark
            if len(line.split('"""')) == 2:
                i += 1
                line = lines[i]
                while ('"""' not in line) and (i < len(lines)):
                    i += 1
                    line = lines[i]
            i += 1
            continue
