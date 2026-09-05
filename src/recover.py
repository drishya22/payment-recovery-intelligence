import random


def choose_recovery_strategy(diagnosis):
    """
    Choose a recovery strategy based on the diagnosed incident type.
    """

    if not diagnosis:
        return None

    strategies = {
    "provider_degradation": "retry_with_fallback_provider",
    "bank_degradation": "retry_after_delay",
    "timeout_spike": "retry_after_delay",
    "payment_method_degradation": "recommend_alternate_method",
    "geographic_degradation": "retry_after_delay"}

    return strategies.get(
        diagnosis["type"],
        "bounded_retry"
    )


def identify_recovery_candidates(events, diagnosis):
    """
    Identify failed payments that are eligible for recovery.
    """

    if not diagnosis:
        return []

    candidates = [
        event
        for event in events
        if (
            diagnosis["start"] <= event.timestamp < diagnosis["end"]
            and getattr(event, diagnosis["dimension"]) == diagnosis["value"]
            and event.status == "failed"
        )
    ]

    return candidates


def choose_fallback_provider(events, degraded_provider):
    """
    Select the healthiest available provider based on observed
    failure rate.

    This is only used when the recovery strategy requires
    a fallback provider.
    """

    provider_stats = {}

    for event in events:

        if event.provider == degraded_provider:
            continue

        if event.provider not in provider_stats:
            provider_stats[event.provider] = {
                "total": 0,
                "failed": 0
            }

        provider_stats[event.provider]["total"] += 1

        if event.status == "failed":
            provider_stats[event.provider]["failed"] += 1

    if not provider_stats:
        return None

    return min(
        provider_stats,
        key=lambda provider:
            provider_stats[provider]["failed"]
            / provider_stats[provider]["total"]
    )


def select_recovery_batch(candidates, max_retries=100):
    """
    Select a bounded batch of failed payments for recovery.

    The retry limit prevents the recovery system from attempting
    an unbounded number of payments.
    """

    return candidates[:max_retries]


def execute_recovery(
    recovery_batch,
    strategy,
    fallback_provider=None
):
    """
    Simulate execution of the selected recovery strategy.

    fallback_provider is only populated when the selected
    strategy uses a fallback provider.
    """

    if not recovery_batch or not strategy:
        return []

    results = []

    for event in recovery_batch:

        # Simulated recovery outcome.
        recovered = random.random() < 0.90

        results.append({
            "transaction_id": event.id,
            "amount": event.amount,
            "original_provider": event.provider,
            "fallback_provider": fallback_provider,
            "strategy": strategy,
            "status": "recovered" if recovered else "failed"
        })

    return results


def verify_recovery(recovery_results):
    """
    Measure the outcome of the recovery execution.
    """

    if not recovery_results:
        return {
            "attempted": 0,
            "recovered": 0,
            "recovered_amount": 0,
            "recovery_rate": 0.0
        }

    recovered = [
        result
        for result in recovery_results
        if result["status"] == "recovered"
    ]

    recovered_amount = sum(
        result["amount"]
        for result in recovered
    )

    return {
        "attempted": len(recovery_results),
        "recovered": len(recovered),
        "recovered_amount": recovered_amount,
        "recovery_rate": (
            len(recovered)
            / len(recovery_results)
            * 100
        )
    }


def create_recovery_audit(
    diagnosis,
    strategy,
    fallback_provider,
    recovery_results
):
    """
    Create an audit record describing the diagnosis,
    recovery strategy, execution and outcome.
    """

    recovered = [
        result
        for result in recovery_results
        if result["status"] == "recovered"
    ]

    recovered_amount = sum(
        result["amount"]
        for result in recovered
    )

    return {
        "incident_type": diagnosis["type"],
        "affected_dimension": diagnosis["dimension"],
        "affected_value": diagnosis["value"],
        "incident_start": diagnosis["start"],
        "incident_end": diagnosis["end"],

        "strategy": strategy,

        "fallback_provider": fallback_provider,

        "retry_attempts": len(recovery_results),
        "recovered_transactions": len(recovered),
        "recovered_amount": recovered_amount,

        "action": strategy
    }