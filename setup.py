from pathlib import Path
from typing import Dict, List, Set

from setuptools import find_packages, setup


def parse_requirements_file(file_path: Path) -> Set[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Requirements file not found: {file_path}")

    requirements = set()
    with file_path.open() as requirements_file:
        for line in requirements_file:
            line = line.strip()
            if line and not line.startswith(("#", "-r", "-c")):
                requirements.add(line)
    return requirements


def get_version_from_constraints(requirement: str, constraints: Set[str]) -> str:
    package_name = requirement.split("==")[0].lower()
    for constraint in constraints:
        if constraint.lower().startswith(f"{package_name.lower()}=="):
            return constraint
    return requirement


def get_requirements() -> Dict[str, List[str]]:
    base_path = Path(__file__).parent / "requirements"

    # Read constraints first
    constraints = parse_requirements_file(base_path / "constraints.txt")

    # Read base requirements
    base_requirements = parse_requirements_file(base_path / "base.txt")
    install_requires = [
        get_version_from_constraints(req, constraints) for req in base_requirements
    ]

    # Read dev requirements
    dev_requirements = parse_requirements_file(base_path / "dev.txt")
    dev_requires = [
        get_version_from_constraints(req, constraints)
        for req in dev_requirements
        if req not in base_requirements  # Avoid duplicates from -r ./base.txt
    ]

    return {"install_requires": install_requires, "dev_requires": dev_requires}


# Get requirements
requirements = get_requirements()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version.txt", "r") as reqs:
    # read only the first line
    version = reqs.readline().strip()

setup(
    author="Steven England",
    author_email="github@steven-england.info",
    description="A package for managing SD cards that are meant to be used in DFROBOT DfPlayer Mini card readers.",
    entry_points={
        "console_scripts": [
            "dfplayer-card-manager=dfplayer_card_manager.cli.cli:app",
        ],
    },
    extras_require={"dev": requirements["dev_requires"]},
    install_requires=requirements["install_requires"],
    license="MIT",
    license_files=["LICENSE"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="dfplayer-card-manager",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/stevenengland/dfplayer_card_manager",
    version=version,
    python_requires=">=3.8",
)
