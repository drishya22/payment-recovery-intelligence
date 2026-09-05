from ai_reasoner import reason_about_recovery


diagnosis = {
    "type": "provider_degradation",
    "dimension": "provider",
    "value": "provider_z",
    "failure_rate": 32.62,
    "baseline_failure_rate": 7.72,
    "relative_increase": 4.22,
    "absolute_increase": 24.90,
    "transaction_count": 371
}


impact = {
    "affected_transactions": 371,
    "failed_transactions": 106,
    "failed_amount": 567051
}


provider_health = {
    "provider_x": {
        "failure_rate": 5.8
    },
    "provider_y": {
        "failure_rate": 4.9
    },
    "provider_z": {
        "failure_rate": 32.62
    }
}


recovery_options = [
    "retry_with_fallback_provider",
    "retry_after_delay",
    "recommend_alternate_method",
    "do_nothing"
]


result = reason_about_recovery(
    diagnosis=diagnosis,
    impact=impact,
    provider_health=provider_health,
    recovery_options=recovery_options
)


print("\nAI Recovery Recommendation")
print("==========================")

for key, value in result.items():
    print(f"{key}: {value}")