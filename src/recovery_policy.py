ALLOWED_STRATEGIES = {
    "provider_degradation": {
        "retry_with_fallback_provider",
        "retry_after_delay",
        "do_nothing"
    },
    "bank_degradation": {
        "retry_after_delay",
        "do_nothing"
    },
    "timeout_spike": {
        "retry_after_delay",
        "do_nothing"
    },
    "payment_method_degradation": {
        "recommend_alternate_method",
        "retry_after_delay",
        "do_nothing"
    },
    "geographic_degradation": {
        "retry_after_delay",
        "do_nothing"
    }
}

MIN_CONFIDENCE = 0.70


def validate_recommendation(
    ai_recommendation,
    diagnosis,
    provider_health
):
    """
    Check whether the AI recommendation is safe to execute.
    """

    if not ai_recommendation or not diagnosis:
        return {
            "approved": False,
            "strategy": "do_nothing",
            "provider": None,
            "reason": "Missing recommendation or diagnosis."
        }

    strategy = ai_recommendation.get(
        "recommended_strategy"
    )

    provider = ai_recommendation.get(
        "recommended_provider"
    )

    confidence = ai_recommendation.get(
        "confidence",
        0
    )

    incident_type = diagnosis["type"]

    allowed_strategies = ALLOWED_STRATEGIES.get(
        incident_type,
        {"do_nothing"}
    )

    # Never execute an action that isn't allowed
    # for the diagnosed incident.
    if strategy not in allowed_strategies:
        return {
            "approved": False,
            "strategy": "do_nothing",
            "provider": None,
            "reason": (
                f"Strategy '{strategy}' is not allowed "
                f"for incident type '{incident_type}'."
            )
        }

    # Low-confidence recommendations should not
    # automatically trigger recovery.
    if confidence < MIN_CONFIDENCE:
        return {
            "approved": False,
            "strategy": "do_nothing",
            "provider": None,
            "reason": (
                f"AI confidence {confidence:.2f} is below "
                f"the minimum threshold of {MIN_CONFIDENCE:.2f}."
            )
        }

    # A fallback provider is only relevant for
    # fallback-provider recovery.
    if strategy == "retry_with_fallback_provider":

        if not provider:
            return {
                "approved": False,
                "strategy": "do_nothing",
                "provider": None,
                "reason": "No fallback provider was recommended."
            }

        if provider not in provider_health:
            return {
                "approved": False,
                "strategy": "do_nothing",
                "provider": None,
                "reason": (
                    f"Recommended provider '{provider}' "
                    f"is not available."
                )
            }

        degraded_provider = diagnosis.get("value")

        if provider == degraded_provider:
            return {
                "approved": False,
                "strategy": "do_nothing",
                "provider": None,
                "reason": (
                    "Fallback provider cannot be the "
                    "provider currently experiencing degradation."
                )
            }

        recommended_failure_rate = provider_health[
            provider
        ]["failure_rate"]

        degraded_failure_rate = provider_health.get(
            degraded_provider,
            {}
        ).get(
            "failure_rate"
        )

        if (
            degraded_failure_rate is not None
            and recommended_failure_rate >= degraded_failure_rate
        ):
            return {
                "approved": False,
                "strategy": "do_nothing",
                "provider": None,
                "reason": (
                    "Recommended fallback provider is not "
                    "healthier than the degraded provider."
                )
            }

    return {
        "approved": True,
        "strategy": strategy,
        "provider": provider,
        "reason": "Recommendation passed recovery policy checks."
    }