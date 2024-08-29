import subprocess  # noqa: S404


def call_black(directory) -> None:
    print("** BLACK **")
    try:
        subprocess.run(["black", directory])  # noqa: S607, S603
    except FileNotFoundError:
        print("Black formatter not found. Please make sure it is installed.")

    print("Calling black completed successfully.")


def call_flake8(directory) -> None:
    print("** FLAKE8 **")
    try:
        subprocess.run(["flake8", directory])  # noqa: S607, S603
    except FileNotFoundError:
        print("flake8 not found. Please make sure it is installed.")

    print("Calling flake8 completed successfully.")


def call_mypy(directory: str) -> None:
    print("** MYPY **")
    try:
        subprocess.run(["mypy", directory])  # noqa: S607, S603
    except FileNotFoundError:
        print("MyPy formatter not found. Please make sure it is installed.")

    print("Calling MyPy completed successfully.")


call_black(".")
call_flake8(".")
call_mypy(".")
