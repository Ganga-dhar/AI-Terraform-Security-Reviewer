from pathlib import Path


def read_terraform_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Terraform file not found: {file_path}"
        )

    if path.suffix not in [".tf", ".tfvars"]:
        raise ValueError(
            "Only Terraform .tf and .tfvars files are supported"
        )

    return path.read_text(encoding="utf-8")