def group_adjacent_anomalies(dimension_anomalies):
    if not dimension_anomalies:
        return []

    groups = {}

    
    for anomaly in dimension_anomalies:
        key = (anomaly["dimension"], anomaly["value"])  # Group anomalies by dimension and value.
        groups.setdefault(key, []).append(anomaly)

    merged_anomalies = []

    for anomalies in groups.values():
        anomalies.sort(key=lambda anomaly: anomaly["start"])

        current=anomalies[0].copy()

        for next_anomaly in anomalies[1:]:
            if next_anomaly["start"]<=current["end"]:
                current["end"]=next_anomaly["end"]
                current["transaction_count"]+=next_anomaly["transaction_count"]

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


def diagnose_incident(dimension_anomalies):
    """
    Identify the most likely cause of a payment degradation.
    """

    if not dimension_anomalies:
        return None

    grouped_anomalies = group_adjacent_anomalies(dimension_anomalies)

    strongest_anomaly = max(
        grouped_anomalies,
        key=lambda anomaly: anomaly["relative_increase"]
    )

    return {
        "type": "payment_degradation",
        "dimension": strongest_anomaly["dimension"],
        "value": strongest_anomaly["value"],
        "start": strongest_anomaly["start"],
        "end": strongest_anomaly["end"],
        "failure_rate": strongest_anomaly["failure_rate"],
        "baseline_failure_rate": strongest_anomaly["baseline_failure_rate"],
        "relative_increase": strongest_anomaly["relative_increase"],
        "absolute_increase": strongest_anomaly["absolute_increase"],
        "transaction_count": strongest_anomaly["transaction_count"]
    }