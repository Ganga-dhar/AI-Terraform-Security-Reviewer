from pathlib import Path


def read_terraform_file(
    file_path: str
) -> str:

    path = Path(
        file_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Terraform file not found: "
            f"{file_path}"
        )

    if path.suffix != ".tf":

        raise ValueError(
            "Provided file is not a "
            "Terraform .tf file"
        )

    return path.read_text(
        encoding="utf-8"
    )