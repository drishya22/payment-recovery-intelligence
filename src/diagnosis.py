def group_adjacent_anomalies(dimension_anomalies):
    """
    Merge adjacent anomalies belonging to the same dimension/value.
    """

    if not dimension_anomalies:
        return []

    groups = {}

    for anomaly in dimension_anomalies:

        key = (
            anomaly["dimension"],
            anomaly["value"]
        )

        groups.setdefault(key, []).append(anomaly)

    merged_anomalies = []

    for anomalies in groups.values():

        anomalies.sort(
            key=lambda anomaly: anomaly["start"]
        )

        current = anomalies[0].copy()

        for next_anomaly in anomalies[1:]:

            if next_anomaly["start"] <= current["end"]:

                current["end"] = next_anomaly["end"]

                current["transaction_count"] += (
                    next_anomaly["transaction_count"]
                )

                current["failure_rate"] = max(
                    current["failure_rate"],
                    next_anomaly["failure_rate"]
                )

                current["absolute_increase"] = max(
                    current["absolute_increase"],
                    next_anomaly["absolute_increase"]
                )

                current["relative_increase"] = max(
                    current["relative_increase"],
                    next_anomaly["relative_increase"]
                )

            else:

                merged_anomalies.append(current)

                current = next_anomaly.copy()

        merged_anomalies.append(current)

    return merged_anomalies


def group_adjacent_failure_reason_anomalies(
    failure_reason_anomalies
):
    """
    Merge adjacent anomalies belonging to the same failure reason.
    """

    if not failure_reason_anomalies:
        return []

    groups = {}

    for anomaly in failure_reason_anomalies:

        reason = anomaly["failure_reason"]

        groups.setdefault(reason, []).append(anomaly)

    merged_anomalies = []

    for anomalies in groups.values():

        anomalies.sort(
            key=lambda anomaly: anomaly["start"]
        )

        current = anomalies[0].copy()

        for next_anomaly in anomalies[1:]:

            if next_anomaly["start"] <= current["end"]:

                current["end"] = next_anomaly["end"]

                current["transaction_count"] += (
                    next_anomaly["transaction_count"]
                )

                current["failure_rate"] = max(
                    current["failure_rate"],
                    next_anomaly["failure_rate"]
                )

                current["absolute_increase"] = max(
                    current["absolute_increase"],
                    next_anomaly["absolute_increase"]
                )

                current["relative_increase"] = max(
                    current["relative_increase"],
                    next_anomaly["relative_increase"]
                )

            else:

                merged_anomalies.append(current)

                current = next_anomaly.copy()

        merged_anomalies.append(current)

    return merged_anomalies


def diagnose_incident(
    dimension_anomalies,
    failure_reason_anomalies=None
):
    """
    Diagnose the most likely payment degradation using
    dimension-level and failure-reason evidence.
    """

    if failure_reason_anomalies is None:
        failure_reason_anomalies = []

    grouped_dimension_anomalies = (
        group_adjacent_anomalies(
            dimension_anomalies
        )
    )

    grouped_reason_anomalies = (
        group_adjacent_failure_reason_anomalies(
            failure_reason_anomalies
        )
    )

    # ---------------------------------------------------------
    # 1. Check for explicit failure-reason evidence
    # ---------------------------------------------------------

    timeout_anomalies = [
        anomaly
        for anomaly in grouped_reason_anomalies
        if anomaly["failure_reason"] == "payment_timeout"
    ]

    if timeout_anomalies:

        strongest_timeout = max(
            timeout_anomalies,
            key=lambda anomaly: anomaly["relative_increase"]
        )

        return {
            "type": "timeout_spike",
            "dimension": "failure_reason",
            "value": strongest_timeout["failure_reason"],
            "start": strongest_timeout["start"],
            "end": strongest_timeout["end"],
            "failure_rate": strongest_timeout["failure_rate"],
            "baseline_failure_rate": strongest_timeout[
                "baseline_failure_rate"
            ],
            "relative_increase": strongest_timeout[
                "relative_increase"
            ],
            "absolute_increase": strongest_timeout[
                "absolute_increase"
            ],
            "transaction_count": strongest_timeout[
                "transaction_count"
            ]
        }

    # ---------------------------------------------------------
    # 2. Diagnose dimension-based degradation
    # ---------------------------------------------------------

    if not grouped_dimension_anomalies:
        return None

    strongest_anomaly = max(
        grouped_dimension_anomalies,
        key=lambda anomaly: anomaly["relative_increase"]
    )

    diagnosis_type_map = {
        "provider": "provider_degradation",
        "bank": "bank_degradation",
        "method": "payment_method_degradation",
        "geo": "geographic_degradation"
    }

    diagnosis_type = diagnosis_type_map.get(
        strongest_anomaly["dimension"],
        "payment_degradation"
    )

    return {
        "type": diagnosis_type,
        "dimension": strongest_anomaly["dimension"],
        "value": strongest_anomaly["value"],
        "start": strongest_anomaly["start"],
        "end": strongest_anomaly["end"],
        "failure_rate": strongest_anomaly["failure_rate"],
        "baseline_failure_rate": strongest_anomaly[
            "baseline_failure_rate"
        ],
        "relative_increase": strongest_anomaly[
            "relative_increase"
        ],
        "absolute_increase": strongest_anomaly[
            "absolute_increase"
        ],
        "transaction_count": strongest_anomaly[
            "transaction_count"
        ]
    }