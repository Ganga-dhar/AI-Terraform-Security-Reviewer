import json
import shutil
import subprocess


def run_checkov(terraform_file: str):

    # -------------------------------------------------
    # Find Checkov executable
    # -------------------------------------------------

    checkov_path = shutil.which(
        "checkov"
    )

    if not checkov_path:

        raise RuntimeError(
            "Checkov executable not found in PATH. "
            "Make sure Checkov is installed in the "
            "active virtual environment."
        )

    # -------------------------------------------------
    # Build Checkov command
    # -------------------------------------------------

    command = [
        checkov_path,
        "-f",
        terraform_file,
        "--framework",
        "terraform",
        "-o",
        "json",
    ]

    # -------------------------------------------------
    # Execute Checkov
    # -------------------------------------------------

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    # -------------------------------------------------
    # Validate output
    # -------------------------------------------------

    if not result.stdout.strip():

        raise RuntimeError(
            "Checkov did not return any output.\n"
            f"Checkov stderr:\n"
            f"{result.stderr}"
        )

    # -------------------------------------------------
    # Parse JSON
    # -------------------------------------------------

    try:

        return json.loads(
            result.stdout
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "Unable to parse Checkov JSON output.\n"
            f"Error: {error}\n"
            f"Checkov output:\n"
            f"{result.stdout}"
        )