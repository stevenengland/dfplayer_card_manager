import glob
import os
import subprocess  # noqa: S404
import sys


def get_os_specific_command_directory() -> str:
    return r".venv\Scripts" if os.name == "nt" else ".venv/bin"


def call_build(argv: list[str]) -> None:
    print("** BUILD **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "python")
    cmd = [cmd_path, "setup.py", "sdist", "bdist_wheel"]
    if argv:
        cmd.extend(argv)
    try:
        subprocess.run(cmd, check=True)  # noqa: S607, S603
    except FileNotFoundError:
        print("Module setup.py not found. Please make sure it is installed.")
        exit(1)

    print("Calling build completed successfully.")


def call_build_check_twine() -> None:
    print("** BUILD CHECK TWINE **")
    cmd_path = os.path.join(get_os_specific_command_directory(), "python")
    cmd = [cmd_path, "-m", "twine", "check", "--strict", f"dist{os.sep}*"]
    subprocess.run(cmd, check=True)  # noqa: S607, S603

    print("Calling twine check completed successfully.")


def call_build_check_wheel() -> None:
    print("** BUILD CHECK WHEEL **")
    wheel_files = glob.glob("dist/*.whl")
    cmd_path = os.path.join(get_os_specific_command_directory(), "check-wheel-contents")
    for wheel in wheel_files:
        cmd = [
            cmd_path,
            wheel,
        ]
        print(f"Checking {wheel}:")
        subprocess.run(cmd, check=True)  # noqa: S607, S603

    print("Calling check-wheel-contents completed successfully.")


call_build(sys.argv[1:])
call_build_check_twine()
call_build_check_wheel()
