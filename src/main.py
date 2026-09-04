from generator import generate_events
from aggregate import aggregate_events
from detector import detect_anomalies, detect_dimension_anomalies_by_window
from diagnosis import diagnose_incident
from impact import calculate_impact
from recover import (
    identify_recovery_candidates,
    choose_fallback_provider,
    select_recovery_batch,
    execute_recovery,
    verify_recovery,
    create_recovery_audit
)


def run_recovery_analysis(num_events=10000):
    """
    Run the complete payment recovery intelligence pipeline.

    Returns:
        A structured result containing detection, diagnosis,
        impact, recovery, verification and audit information.
    """

    # 1. Generate payment events
    events = generate_events(num_events)

    # 2. Aggregate payment metrics
    metrics = aggregate_events(events)

    # 3. Detect system-wide anomalies
    anomalies = detect_anomalies(events)

    # 4. Detect dimension-specific anomalies
    provider_anomalies = detect_dimension_anomalies_by_window(
        events,
        dimension="provider"
    )

    # 5. Diagnose the incident
    diagnosis = diagnose_incident(provider_anomalies)

    if not diagnosis:
        return {
            "metrics": metrics,
            "anomalies": anomalies,
            "provider_anomalies": provider_anomalies,
            "diagnosis": None,
            "impact": None,
            "recovery": None,
            "verification": None,
            "audit": None
        }

    # 6. Calculate impact
    impact = calculate_impact(events, diagnosis)

    # 7. Choose fallback provider
    fallback_provider = choose_fallback_provider(
        events,
        diagnosis["value"]
    )

    # 8. Identify recovery candidates
    candidates = identify_recovery_candidates(
        events,
        diagnosis
    )

    # 9. Apply recovery limit
    recovery_batch = select_recovery_batch(candidates)

    # 10. Execute recovery
    recovery_results = execute_recovery(
        recovery_batch,
        fallback_provider
    )

    # 11. Verify recovery
    verification = verify_recovery(
        recovery_results
    )

    # 12. Create audit record
    audit = create_recovery_audit(
        diagnosis,
        fallback_provider,
        recovery_results
    )

    return {
        "metrics": metrics,
        "anomalies": anomalies,
        "provider_anomalies": provider_anomalies,
        "diagnosis": diagnosis,
        "impact": impact,
        "recovery": {
            "degraded_provider": diagnosis["value"],
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
    result = run_recovery_analysis()

    print("\nPayment Recovery Intelligence")
    print("============================")

    print("\nPayment Summary")
    print("----------------")
    print(f"Total transactions : {result['metrics']['total_transactions']}")
    print(f"Successful         : {result['metrics']['successful_transactions']}")
    print(f"Failed             : {result['metrics']['failed_transactions']}")
    print(f"Success rate       : {result['metrics']['success_rate']:.2f}%")
    print(f"Failure rate       : {result['metrics']['failure_rate']:.2f}%")

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
        print(f"Affected transactions : {impact['affected_transactions']}")
        print(f"Failed transactions   : {impact['failed_transactions']}")
        print(f"Payment value at risk : ₹{impact['failed_amount']}")

    print("\nRecovery")
    print("----------------")

    recovery = result["recovery"]

    if recovery:
        print(f"Degraded provider : {recovery['degraded_provider']}")
        print(f"Fallback provider : {recovery['fallback_provider']}")
        print(f"Recovery candidates : {recovery['candidates']}")
        print(f"Selected for retry  : {recovery['selected_for_retry']}")

    print("\nRecovery Verification")
    print("---------------------")

    verification = result["verification"]

    if verification:
        print(f"Attempts        : {verification['attempted']}")
        print(f"Recovered       : {verification['recovered']}")
        print(f"Recovery rate   : {verification['recovery_rate']:.2f}%")
        print(f"Recovered value : ₹{verification['recovered_amount']}")

    print("\nRecovery Audit")
    print("--------------")

    audit = result["audit"]

    if audit:
        print(f"Action           : {audit['action']}")
        print(f"Original provider: {audit['original_provider']}")
        print(f"Fallback provider: {audit['fallback_provider']}")
        print(f"Retry attempts   : {audit['retry_attempts']}")
        print(f"Recovered        : {audit['recovered_transactions']}")
        print(f"Recovered value  : ₹{audit['recovered_amount']}")