import random
from datetime import datetime

from generator import generate_events
from aggregate import aggregate_events

from detector import (
    detect_anomalies,
    detect_dimension_anomalies_by_window,
    detect_failure_reason_anomalies
)

from diagnosis import diagnose_incident
from impact import calculate_impact

from provider_health import calculate_provider_health
from ai_reasoner import reason_about_recovery
from recovery_policy import validate_recommendation

from recover import (
    identify_recovery_candidates,
    select_recovery_batch,
    execute_recovery,
    verify_recovery,
    create_recovery_audit
)


def run_recovery_analysis(
    num_events=10000,
    seed=42,
    scenario="provider_degradation"
):
    """
    Run the complete payment recovery pipeline.
    """

    # Keep the demo reproducible
    random.seed(seed)

    events = generate_events(
        num_events=num_events,
        start_time=datetime(2026, 9, 3, 9, 0, 0),
        duration_hours=9,
        scenario=scenario
    )

    # Basic payment metrics
    metrics = aggregate_events(events)

    # Detect overall spikes in failure rate
    anomalies = detect_anomalies(events)

    # Check different dimensions for localized degradation.
    dimension_anomalies = []

    for dimension in ["provider", "bank", "method", "geo"]:
        detected = detect_dimension_anomalies_by_window(
            events,
            dimension=dimension
        )

        dimension_anomalies.extend(detected)

    # Look for spikes in specific failure reasons,
    # such as payment timeouts or bank errors.
    failure_reason_anomalies = detect_failure_reason_anomalies(
        events
    )

    # Combine the detected signals and determine
    # the most likely incident.
    diagnosis = diagnose_incident(
        dimension_anomalies,
        failure_reason_anomalies
    )

    if not diagnosis:
        return {
            "scenario": scenario,
            "metrics": metrics,
            "anomalies": anomalies,
            "dimension_anomalies": dimension_anomalies,
            "failure_reason_anomalies": failure_reason_anomalies,
            "diagnosis": None,
            "impact": None,
            "provider_health": None,
            "ai_recommendation": None,
            "policy": None,
            "recovery": None,
            "verification": None,
            "audit": None
        }

    # Estimate how much payment value was affected.
    impact = calculate_impact(
        events,
        diagnosis
    )

    # Calculate provider health from the observed payment data.
    provider_health = calculate_provider_health(events)

    recovery_options = [
        "retry_with_fallback_provider",
        "retry_after_delay",
        "recommend_alternate_method",
        "do_nothing"
    ]

    # Gemini reasons over the evidence and recommends
    # the most appropriate recovery action.
    ai_recommendation = reason_about_recovery(
        diagnosis=diagnosis,
        impact=impact,
        provider_health=provider_health,
        recovery_options=recovery_options
    )

    # The AI recommendation is checked by deterministic
    # recovery rules before anything can be executed.
    policy_result = validate_recommendation(
        ai_recommendation=ai_recommendation,
        diagnosis=diagnosis,
        provider_health=provider_health
    )

    strategy = policy_result["strategy"]
    fallback_provider = policy_result["provider"]

    # Find failed payments affected by the diagnosed incident.
    candidates = identify_recovery_candidates(
        events,
        diagnosis
    )

    # Keep the recovery batch bounded.
    recovery_batch = select_recovery_batch(
        candidates
    )

    recovery_results = execute_recovery(
        recovery_batch,
        strategy,
        fallback_provider
    )

    # Measure the actual recovery outcome.
    verification = verify_recovery(
        recovery_results
    )

    # Store the recovery decision and result for auditing.
    audit = create_recovery_audit(
        diagnosis,
        strategy,
        fallback_provider,
        recovery_results
    )

    return {
        "scenario": scenario,
        "metrics": metrics,
        "anomalies": anomalies,
        "dimension_anomalies": dimension_anomalies,
        "failure_reason_anomalies": failure_reason_anomalies,
        "diagnosis": diagnosis,
        "impact": impact,
        "provider_health": provider_health,
        "ai_recommendation": ai_recommendation,
        "policy": policy_result,
        "recovery": {
            "strategy": strategy,
            "affected_value": diagnosis["value"],
            "fallback_provider": fallback_provider,
            "candidates": len(candidates),
            "selected_for_retry": len(recovery_batch),
            "attempted": verification["attempted"],
            "recovered": verification["recovered"],
            "recovered_amount": verification["recovered_amount"],
            "recovery_rate": verification["recovery_rate"]
        },
        "verification": verification,
        "audit": audit
    }


if __name__ == "__main__":

    result = run_recovery_analysis(
        scenario="timeout_spike"
    )

    print("\nPayment Recovery Intelligence")
    print("============================")

    print("\nPayment Summary")
    print("----------------")

    print(
        f"Total transactions : "
        f"{result['metrics']['total_transactions']}"
    )

    print(
        f"Successful         : "
        f"{result['metrics']['successful_transactions']}"
    )

    print(
        f"Failed             : "
        f"{result['metrics']['failed_transactions']}"
    )

    print(
        f"Success rate       : "
        f"{result['metrics']['success_rate']:.2f}%"
    )

    print(
        f"Failure rate       : "
        f"{result['metrics']['failure_rate']:.2f}%"
    )

    print("\nIncident Diagnosis")
    print("------------------")

    diagnosis = result["diagnosis"]

    if diagnosis:
        print(f"Type       : {diagnosis['type']}")
        print(f"Dimension  : {diagnosis['dimension']}")
        print(f"Value      : {diagnosis['value']}")
        print(f"Failure    : {diagnosis['failure_rate']:.2f}%")
        print(f"Baseline   : {diagnosis['baseline_failure_rate']:.2f}%")
        print(f"Increase   : {diagnosis['absolute_increase']:.2f} pp")
        print(f"Relative   : {diagnosis['relative_increase']:.2f}x")
    else:
        print("No incident diagnosed.")

    print("\nImpact Analysis")
    print("----------------")

    impact = result["impact"]

    if impact:
        print(
            f"Affected transactions : "
            f"{impact['affected_transactions']}"
        )

        print(
            f"Failed transactions   : "
            f"{impact['failed_transactions']}"
        )

        print(
            f"Failed payment value  : "
            f"₹{impact['failed_amount']}"
        )

    print("\nAI Recovery Reasoning")
    print("---------------------")

    ai_recommendation = result["ai_recommendation"]

    if ai_recommendation:
        print(
            f"Recommended strategy : "
            f"{ai_recommendation['recommended_strategy']}"
        )

        print(
            f"Recommended provider : "
            f"{ai_recommendation['recommended_provider']}"
        )

        print(
            f"Reasoning            : "
            f"{ai_recommendation['reasoning']}"
        )

        print(
            f"Confidence           : "
            f"{ai_recommendation['confidence']}"
        )

        print(
            f"Risk                 : "
            f"{ai_recommendation['risk']}"
        )

        print(
            f"Expected recovery    : "
            f"{ai_recommendation['expected_recovery']}"
        )

    print("\nRecovery Policy")
    print("----------------")

    policy = result["policy"]

    if policy:
        print(
            f"Approved             : "
            f"{policy['approved']}"
        )

        print(
            f"Strategy             : "
            f"{policy['strategy']}"
        )

        print(
            f"Provider             : "
            f"{policy['provider']}"
        )

        print(
            f"Policy decision      : "
            f"{policy['reason']}"
        )

    print("\nRecovery")
    print("----------------")

    recovery = result["recovery"]

    if recovery:
        print(
            f"Strategy            : "
            f"{recovery['strategy']}"
        )

        print(
            f"Affected value      : "
            f"{recovery['affected_value']}"
        )

        print(
            f"Fallback provider   : "
            f"{recovery['fallback_provider']}"
        )

        print(
            f"Recovery candidates : "
            f"{recovery['candidates']}"
        )

        print(
            f"Selected for retry  : "
            f"{recovery['selected_for_retry']}"
        )

    print("\nRecovery Verification")
    print("---------------------")

    verification = result["verification"]

    if verification:
        print(
            f"Attempts        : "
            f"{verification['attempted']}"
        )

        print(
            f"Recovered       : "
            f"{verification['recovered']}"
        )

        print(
            f"Recovery rate   : "
            f"{verification['recovery_rate']:.2f}%"
        )

        print(
            f"Recovered value : "
            f"₹{verification['recovered_amount']}"
        )

    print("\nRecovery Audit")
    print("--------------")

    audit = result["audit"]

    if audit:
        print(
            f"Incident type     : "
            f"{audit['incident_type']}"
        )

        print(
            f"Affected          : "
            f"{audit['affected_dimension']} = "
            f"{audit['affected_value']}"
        )

        print(
            f"Action            : "
            f"{audit['action']}"
        )

        print(
            f"Fallback provider : "
            f"{audit['fallback_provider']}"
        )

        print(
            f"Retry attempts    : "
            f"{audit['retry_attempts']}"
        )

        print(
            f"Recovered         : "
            f"{audit['recovered_transactions']}"
        )

        print(
            f"Recovered value   : "
            f"₹{audit['recovered_amount']}"
        )