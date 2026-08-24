import json
import sys
from pathlib import Path

from auditor.checkov_parser import parse_checkov_results
from auditor.checkov_runner import run_checkov
from auditor.llm_client import create_client
from auditor.parser import read_terraform_file
from auditor.security_gate import evaluate_security_gate


def load_prompt() -> str:
    prompt_path = Path(
        "prompts/terraform_security.txt"
    )

    return prompt_path.read_text(
        encoding="utf-8"
    )


def audit_terraform(file_path: str):

    # -------------------------------------------------
    # 1. Read Terraform
    # -------------------------------------------------

    terraform_code = read_terraform_file(
        file_path
    )

    # -------------------------------------------------
    # 2. Load security prompt
    # -------------------------------------------------

    security_prompt = load_prompt()

    # -------------------------------------------------
    # 3. Run Checkov automatically
    # -------------------------------------------------

    checkov_data = run_checkov(
        file_path
    )

    # -------------------------------------------------
    # 4. Parse Checkov findings
    # -------------------------------------------------

    checkov_findings = parse_checkov_results(
        checkov_data
    )

    # -------------------------------------------------
    # 5. Evaluate deterministic security gate
    # -------------------------------------------------

    security_gate = evaluate_security_gate(
        checkov_findings
    )

    # -------------------------------------------------
    # 6. Convert Checkov findings to JSON
    # -------------------------------------------------

    checkov_context = json.dumps(
        checkov_findings,
        indent=2
    )

    # -------------------------------------------------
    # 7. Create Bedrock client
    # -------------------------------------------------

    client = create_client()

    # -------------------------------------------------
    # 8. Send Terraform + Checkov findings to Nova
    # -------------------------------------------------

    response = client.converse(
        modelId="amazon.nova-lite-v1:0",

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": (
                            f"{security_prompt}\n\n"

                            "Review the following Terraform "
                            "configuration.\n\n"

                            "```terraform\n"
                            f"{terraform_code}\n"
                            "```\n\n"

                            "The following deterministic "
                            "security findings were generated "
                            "by Checkov.\n\n"

                            "```json\n"
                            f"{checkov_context}\n"
                            "```\n\n"

                            "Validate the Checkov findings "
                            "against the Terraform code.\n\n"

                            "Do not blindly classify every "
                            "Checkov finding as a vulnerability.\n\n"

                            "Provide contextual security "
                            "analysis and remediation guidance."
                        )
                    }
                ],
            }
        ],

        inferenceConfig={
            "maxTokens": 3000,
            "temperature": 0,
        },
    )

    # -------------------------------------------------
    # 9. Extract Nova response
    # -------------------------------------------------

    result = response[
        "output"
    ][
        "message"
    ][
        "content"
    ][0]["text"]

    # -------------------------------------------------
    # 10. Remove Markdown code fences
    # -------------------------------------------------

    result = result.strip()

    if result.startswith("```json"):

        result = result[
            len("```json"):
        ].strip()

    elif result.startswith("```"):

        result = result[
            len("```"):
        ].strip()

    if result.endswith("```"):

        result = result[
            :-3
        ].strip()

    # -------------------------------------------------
    # 11. Parse AI JSON
    # -------------------------------------------------

    try:

        ai_result = json.loads(
            result
        )

    except json.JSONDecodeError:

        return {
            "status": "ERROR",

            "summary": (
                "LLM returned invalid JSON"
            ),

            "security_gate": security_gate,

            "raw_response": result,
        }

    # -------------------------------------------------
    # 12. Add deterministic security gate
    # -------------------------------------------------

    ai_result[
        "security_gate"
    ] = security_gate

    # -------------------------------------------------
    # 13. Make overall status follow security gate
    # -------------------------------------------------

    if security_gate["status"] == "FAIL":

        ai_result["status"] = "FAIL"

    return ai_result


if __name__ == "__main__":

    # -------------------------------------------------
    # Validate command-line arguments
    # -------------------------------------------------

    if len(sys.argv) != 2:

        print(
            "Usage: "
            "python -m auditor.auditor "
            "<terraform-file>"
        )

        sys.exit(1)

    terraform_file = sys.argv[1]

    try:

        result = audit_terraform(
            terraform_file
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        # ---------------------------------------------
        # CI/CD exit code
        # ---------------------------------------------

        if (
            result.get(
                "security_gate",
                {}
            ).get(
                "status"
            ) == "FAIL"
        ):

            sys.exit(1)

        sys.exit(0)

    except Exception as error:

        print(
            json.dumps(
                {
                    "status": "ERROR",
                    "error": str(error),
                },
                indent=2,
            )
        )

        sys.exit(1)