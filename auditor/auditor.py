import json
from pathlib import Path

from auditor.llm_client import create_client
from auditor.parser import read_terraform_file


def load_prompt() -> str:
    prompt_path = Path("prompts/terraform_security.txt")

    return prompt_path.read_text(encoding="utf-8")


def audit_terraform(file_path: str):

    terraform_code = read_terraform_file(file_path)
    security_prompt = load_prompt()

    client = create_client()

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": security_prompt,
            },
            {
                "role": "user",
                "content": (
                    "Review the following Terraform code.\n\n"
                    f"```terraform\n{terraform_code}\n```"
                ),
            },
        ],
    )

    result = response.output_text

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "status": "ERROR",
            "raw_response": result,
        }

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(
            "Usage: python -m auditor.auditor <terraform-file>"
        )
        sys.exit(1)

    terraform_file = sys.argv[1]

    result = audit_terraform(terraform_file)

    print(json.dumps(result, indent=2))


    #python -m auditor.auditor examples/vulnerable.tf