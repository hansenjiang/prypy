"""Objects representing notable Python code features.
"""


# Imports


from __future__ import annotations
from typing import Any, Self, Union, Optional
from pathlib import Path
import operator

from prypy import utils


# Classes


## Module


class Variable:
    def __init__(
        self,
        name: str,
        type: type,
        value: Optional[Any],
        parent: Union[Function, Class, Module],
    ):
        self.name = name
        self.type = type
        self.value = value
        self.parent = parent

    @classmethod
    def from_line(cls, line: str, parent: Package) -> Self:
        # TODO resolve unknown types

        if ":" in line:
            constant_name = line.split(":")[0].strip()
            constant_type = line.split(":")[1].split("=")[0].strip()
        else:
            constant_name = line.split("=")[0].strip()
            constant_type = None
        constant_value = line.split("=")[1].strip()
        return Variable(constant_name, constant_type, constant_value, parent)


class Function:
    def __init__(
        self,
        name: str,
        input: list[Variable],
        output: list[Variable],
        calls: list[Self],
        lines: int,
        parent: Union[Self, Class, Module],
    ) -> None:
        self.name = name
        self.input = input
        self.output = output
        self.calls = calls
        self.lines = lines
        self.parent = parent


class Class:
    def __init__(
        self,
        name: str,
        class_attributes: list[Variable],
        instance_attributes: list[Variable],
        functions: list[Function],
        parent: Module,
    ) -> None:
        self.name = name
        self.class_attributes = class_attributes
        self.instance_attributes = instance_attributes
        self.functions = functions
        self.parent = parent


## Package


class Module:
    def __init__(
        self,
        name: str,
        imports: list[Self],
        constants: list[Variable],
        classes: list[Class],
        functions: list[Function],
        parent: Package,
    ):
        self.name = name
        self.imports = imports
        self.constants = constants
        self.classes = classes
        self.functions = functions
        self.parent = parent

    @classmethod
    def from_path(cls, path: Path, parent: Package) -> Self:
        # TODO remove
        print(path)

        module = Module(path.stem, [], [], [], [], parent)

        # Store code as list[str] with trimmed newline character
        lines = [
            line[:-1] if len(line) > 0 else line
            for line in open(path, mode="r").readlines()
        ]
        tab_levels = [module]

        # Iterate over each line of code
        i = 0
        while i < len(lines):
            line = lines[i]

            # TODO remove
            print(i, line)

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
                    module.constants.append(
                        Variable(constant_name, str, constant_str, module)
                    )

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

            # Handle beginning of file - assume only imports and constants
            if utils.tab_level(line) == 0:
                # TODO implement imports
                # Add imports
                if "import " in line:
                    if "from " in line:
                        pass
                    else:
                        pass

                # Add constants
                if ("=" in line) and ("(" not in line):
                    module.constants.append(Variable.from_line(line, module))

            # Add classes
            elif "class " in line:
                # If class inherits
                if "(" in line:
                    class_name = line.split("class")[1].split("(")[0].strip()
                else:
                    class_name = line.split("class")[1].split(":")[0].strip()

                i += 1
                line = lines[i]
                while (
                    (utils.tab_level(line) == 1)
                    and (len(line.strip()) > 0)
                    and (i < len(lines))
                ):
                    i += 1
                    line = lines[i]

                #
                tab_levels.append(class_name)
                tab_levels = [module]

            # Add functions
            elif "def " in line:
                pass

            i += 1

        return module


class Package:
    def __init__(
        self,
        name: str,
        modules: list[Module],
        subpackages: list[Self],
        parent: Union[Repository, Self],
    ):
        self.name = name
        self.modules = modules
        self.subpackages = subpackages
        self.parent = parent

    def __str__(self) -> str:
        pkg_str = f"{self.name}\n"
        corner = "├"

        # Only return name if package contains no modules or subpackages
        if len(self.modules) == 0 and len(self.subpackages) == 0:
            return pkg_str

        # Iterate over subpackages
        for subpackage in self.subpackages:
            if (subpackage.name == self.subpackages[-1].name) and (
                len(self.modules) == 0
            ):
                corner = "└"
            pkg_str += f"{corner}─── {subpackage.name}\n"
            pkg_str += "\n".join(
                ["│    " + str_line for str_line in str(subpackage).split("\n")[1:-1]]
            )
            pkg_str += "\n"

        # Iterate over modules
        for module in self.modules:
            if module.name == self.modules[-1].name:
                corner = "└"
            pkg_str += f"{corner}─── {module.name}\n"

        # Return str representing package
        return pkg_str

    @classmethod
    def from_path(cls, path: Path, parent: Union[Package, Repository]) -> Self:
        package = Package(path.name, [], [], parent)
        item_paths = utils.get_item_paths(path)

        # Raise error if not package
        if "__init__.py" not in utils.get_item_names(path):
            raise ValueError(f"Expected __init__ module in package {path.name}.")

        # Iterate over each item in directory
        for item in item_paths:
            # If item is directory, it may be a subpackage
            if item.is_dir():
                # Add item if subpackage and skip otherwise
                try:
                    package.subpackages.append(Package.from_path(item, package))
                except ValueError:
                    pass

            # Add python files and skip others
            else:
                if item.suffix == ".py":
                    package.modules.append(Module.from_path(item, package))

        # Sort items by name
        package.subpackages.sort(key=operator.attrgetter("name"))
        package.modules.sort(key=operator.attrgetter("name"))

        # Return primary package
        return package


class Repository:
    def __init__(self, name: str, source: Package, path: Path):
        self.name = name
        self.source = source
        self.path = path

    def __str__(self) -> str:
        repo_str = f"\n══════════ {self.name} ══════════\n"
        repo_str += f"{str(self.source)}"
        return repo_str

    @classmethod
    def from_path(cls, path: Path) -> Self:
        repository = Repository(path.name, None, path)
        items = utils.get_item_paths(path)

        # Assume repository structure of `[repo-name]/src/[repo_name]`
        src_name = "src"
        if src_name in [item.name for item in items]:
            src_items = utils.get_item_names((path / src_name))
            package_name = "_".join(path.name.split("-"))

            # Raise error if `repo_name` package not found
            if package_name in src_items:
                repository.source = Package.from_path(
                    (path / src_name / package_name), repository
                )
            else:
                raise ValueError(
                    f"Expected source package {package_name} not found in repository {path.name}."
                )
        else:
            raise NotImplementedError(
                f"No source package discovered in repository {path.name}."
            )

        return repository


if __name__ == "__main__":
    path = Path("/home/hansen/projects/gjw/morse/morse-pipeline").resolve()
    repo = Repository.from_path(path)
    print(repo)
