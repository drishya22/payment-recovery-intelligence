def calculate_provider_health(events):
    """
    Calculate observed failure rates for each payment provider.
    """

    provider_stats = {}

    for event in events:
        if event.provider not in provider_stats:
            provider_stats[event.provider] = {
                "total": 0,
                "failed": 0
            }

        provider_stats[event.provider]["total"] += 1

        if event.status == "failed":
            provider_stats[event.provider]["failed"] += 1

    provider_health = {}

    for provider, stats in provider_stats.items():
        failure_rate = (
            stats["failed"] / stats["total"] * 100
            if stats["total"] > 0
            else 0.0
        )

        provider_health[provider] = {
            "total_transactions": stats["total"],
            "failed_transactions": stats["failed"],
            "failure_rate": failure_rate
        }

    return provider_health