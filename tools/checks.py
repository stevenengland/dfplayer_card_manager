import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return ".venv/Scripts" if os.name == "nt" else ".venv/bin"


def call_black(directory) -> None:
    print("** BLACK **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "black")
    try:
        result_subprocess = subprocess.run(
            [cmd_path, directory], check=True
        )  # noqa: S607, S603

    except FileNotFoundError:
        print("Black formatter not found. Please make sure it is installed.")

    if result_subprocess.returncode != 0:
        raise RuntimeError(
            f"Black formatter failed with return code {result_subprocess.returncode}",
        )

    print("Calling black completed successfully.")


def call_flake8(directory) -> None:
    print("** FLAKE8 **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "flake8")
    try:
        result_subprocess = subprocess.run([cmd_path, directory])  # noqa: S607, S603
    except FileNotFoundError:
        print("flake8 not found. Please make sure it is installed.")

    if result_subprocess.returncode != 0:
        raise RuntimeError(
            f"flake8 failed with return code {result_subprocess.returncode}",
        )

    print("Calling flake8 completed successfully.")


def call_mypy(directory: str) -> None:
    print("** MYPY **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "mypy")
    try:
        result_subprocess = subprocess.run(  # noqa: S607, S603
            [cmd_path, directory, "--cache-dir=nul"],
            check=True,
        )

    except FileNotFoundError:
        print("MyPy formatter not found. Please make sure it is installed.")

    if result_subprocess.returncode != 0:
        raise RuntimeError(
            f"MyPy failed with return code {result_subprocess.returncode}",
        )

    print("Calling MyPy completed successfully.")


if len(sys.argv) > 1:  # noqa: C901
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
    error_count = 0
    try:
        call_black(".")
    except Exception as black_error:
        print(black_error)
        error_count += 1
    try:
        call_flake8(".")
    except Exception as flake8_error:
        print(flake8_error)
        error_count += 1
    try:
        call_mypy(".")
    except Exception as mypy_error:
        print(mypy_error)
        error_count += 1

    if error_count > 0:
        exit(1)
