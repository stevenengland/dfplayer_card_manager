import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return ".venv/Scripts" if os.name == "nt" else ".venv/bin"


def call_pytest() -> None:
    print("** PYTEST **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "pytest")
    try:
        subprocess.run([cmd_path])  # noqa: S607, S603
    except FileNotFoundError:
        print("PyTest not found. Please make sure it is installed.")

    print("Calling PyTest completed successfully.")


def call_pytest_e2e() -> None:
    print("** PYTEST **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "pytest")
    try:
        subprocess.run([cmd_path, "--e2e"])  # noqa: S607, S603
    except FileNotFoundError:
        print("PyTest not found. Please make sure it is installed.")

    print("Calling PyTest completed successfully.")


if len(sys.argv) > 1:
    argument = sys.argv[1]
    if argument == "e2e":
        call_pytest_e2e()
    else:
        print("Invalid argument. Please specify 'black', 'flake8', or 'mypy'.")
        exit(1)
else:
    call_pytest()
