BLOCKING_SEVERITIES = {
    "CRITICAL",
    "HIGH",
}


def evaluate_security_gate(result: dict) -> bool:
    findings = result.get("findings", [])

    for finding in findings:
        severity = finding.get("severity", "").upper()

        if severity in BLOCKING_SEVERITIES:
            return False

    return True