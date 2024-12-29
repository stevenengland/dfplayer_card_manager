import os
import shutil
import subprocess  # noqa: S404
import sys
from pathlib import Path


def main() -> None:  # noqa: WPS213
    # Check if running inside a virtual environment
    if "VIRTUAL_ENV" in os.environ:
        print("Active venv session detected. Please call 'deactivate' first.")
        sys.exit(1)

    # Check if python3 is available
    if shutil.which("python3") is None:
        print("python3 could not be found. Please install it first.")
        sys.exit(1)

    # Set base directory
    base_dir = Path(__file__).resolve().parent.parent
    venv_dir = base_dir / ".venv"

    # Delete old virtual environment
    print(f">> Deleting old virtual environment folder: {venv_dir}")
    if venv_dir.exists() and venv_dir.is_dir():
        shutil.rmtree(venv_dir)

    # Create new virtual environment
    print(">> Creating new virtual environment folder")
    subprocess.run(  # noqa: S607, S603
        [sys.executable, "-m", "venv", str(venv_dir)],
        check=True,
    )

    # Install dependencies
    print(">> Installing dependencies")

    if os.name == "posix":
        subprocess.run(  # noqa: S607, S603
            [str(venv_dir / "bin" / "pip"), "install", "-e", f"{str(base_dir)}[dev]"],
            check=True,
        )
    else:
        subprocess.run(  # noqa: S607, S603
            [
                str(venv_dir / "Scripts" / "pip"),
                "install",
                "-e",
                f"{str(base_dir)}[dev]",
            ],
            check=True,
        )

    print(">> Done")


if __name__ == "__main__":
    main()
