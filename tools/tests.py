import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return r".venv\Scripts" if os.name == "nt" else ".venv/bin"


def call_pytest() -> None:
    print("** PYTEST **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "python")
    try:
        subprocess.run([cmd_path, "-m", "pytest", "."])  # noqa: S607, S603
    except FileNotFoundError:
        print("Module pytest not found. Please make sure it is installed.")

    print("Calling PyTest completed successfully.")


def call_pytest_e2e() -> None:
    print("** PYTEST **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "python")
    try:
        subprocess.run([cmd_path, "-m", "pytest", ".", "--e2e"])  # noqa: S607, S603
    except FileNotFoundError:
        print("Module pytest not found. Please make sure it is installed.")

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
