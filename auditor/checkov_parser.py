def parse_checkov_results(data):

    """
    Extract failed Checkov checks from
    Checkov JSON output.
    """

    failed_checks = []

    results = data.get(
        "results",
        {}
    )

    for check in results.get(
        "failed_checks",
        []
    ):

        failed_checks.append(
            {
                "check_id": check.get(
                    "check_id"
                ),

                "check_name": check.get(
                    "check_name"
                ),

                "resource": check.get(
                    "resource"
                ),

                "file_path": check.get(
                    "file_path"
                ),

                "file_line_range": check.get(
                    "file_line_range"
                ),

                "guideline": check.get(
                    "guideline"
                ),
            }
        )

    return failed_checks