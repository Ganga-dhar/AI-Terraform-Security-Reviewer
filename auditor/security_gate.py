def evaluate_security_gate(findings):

    """
    Deterministic security gate.

    Any failed Checkov security check causes
    the pipeline to fail.

    The LLM is NOT responsible for deciding
    whether the pipeline should fail.
    """

    if findings:

        return {
            "status": "FAIL",

            "reason": (
                "Checkov security checks failed"
            ),

            "failed_checks": len(
                findings
            ),

            "findings": findings,
        }

    return {
        "status": "PASS",

        "reason": (
            "No Checkov security checks failed"
        ),

        "failed_checks": 0,

        "findings": [],
    }