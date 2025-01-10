import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return r".venv\Scripts" if os.name == "nt" else ".venv/bin"


def call_pytest(argv: list[str]) -> None:
    print("** PYTEST **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "python")
    cmd = [cmd_path, "-m", "pytest", "."]
    if argv:
        cmd.extend(argv)
    try:
        subprocess.run(cmd, check=True)  # noqa: S607, S603
    except FileNotFoundError:
        print("Module pytest not found. Please make sure it is installed.")
        exit(1)

    print("Calling PyTest completed successfully.")


call_pytest(sys.argv[1:])
