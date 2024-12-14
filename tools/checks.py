import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return ".venv/Scripts" if os.name == "nt" else ".venv/bin"


def call_black(directory) -> None:
    print("** BLACK **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "black")
    try:
        result = subprocess.run([cmd_path, directory])  # noqa: S607, S603
        if result.returncode != 0:
            raise Exception(
                f"Black formatter failed with return code {result.returncode}"
            )

    except FileNotFoundError:
        print("Black formatter not found. Please make sure it is installed.")

    print("Calling black completed successfully.")


def call_flake8(directory) -> None:
    print("** FLAKE8 **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "flake8")
    try:
        result = subprocess.run([cmd_path, directory])  # noqa: S607, S603
        if result.returncode != 0:
            raise Exception(f"flake8 failed with return code {result.returncode}")
    except FileNotFoundError:
        print("flake8 not found. Please make sure it is installed.")

    print("Calling flake8 completed successfully.")


def call_mypy(directory: str) -> None:
    print("** MYPY **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "mypy")
    try:
        result = subprocess.run([cmd_path, directory])  # noqa: S607, S603
        if result.returncode != 0:
            raise Exception(f"MyPy failed with return code {result.returncode}")
    except FileNotFoundError:
        print("MyPy formatter not found. Please make sure it is installed.")

    print("Calling MyPy completed successfully.")


if len(sys.argv) > 1:
    argument = sys.argv[1]
    if argument == "black":
        call_black(".")
    elif argument == "flake8":
        call_flake8(".")
    elif argument == "mypy":
        call_mypy(".")
    else:
        print("Invalid argument. Please specify 'black', 'flake8', or 'mypy'.")
        exit(1)
else:
    call_black(".")
    call_flake8(".")
    call_mypy(".")
