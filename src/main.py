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

from recover import (
    choose_recovery_strategy,
    identify_recovery_candidates,
    choose_fallback_provider,
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
    Run the complete payment recovery intelligence pipeline.

    Args:
        num_events: Number of synthetic payment events to generate.
        seed: Random seed for reproducible simulation.
        scenario: Incident scenario to simulate.

    Returns:
        A structured result containing detection, diagnosis,
        impact, recovery, verification and audit information.
    """

    random.seed(seed)

    # ---------------------------------------------------------
    # 1. Generate payment events
    # ---------------------------------------------------------

    events = generate_events(
        num_events=num_events,
        start_time=datetime(2026, 9, 3, 9, 0, 0),
        duration_hours=9,
        scenario=scenario
    )

    # ---------------------------------------------------------
    # 2. Aggregate payment metrics
    # ---------------------------------------------------------

    metrics = aggregate_events(events)

    # ---------------------------------------------------------
    # 3. Detect system-wide anomalies
    # ---------------------------------------------------------

    anomalies = detect_anomalies(events)

    # ---------------------------------------------------------
    # 4. Detect dimension-specific anomalies
    # ---------------------------------------------------------

    dimension_anomalies = []

    for dimension in ["provider", "bank", "method", "geo"]:

        detected = detect_dimension_anomalies_by_window(
            events,
            dimension=dimension
        )

        dimension_anomalies.extend(detected)

    # ---------------------------------------------------------
    # 5. Detect failure-reason anomalies
    # ---------------------------------------------------------

    failure_reason_anomalies = detect_failure_reason_anomalies(
        events
    )

    # ---------------------------------------------------------
    # 6. Diagnose the incident
    # ---------------------------------------------------------

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
            "recovery": None,
            "verification": None,
            "audit": None
        }

    # ---------------------------------------------------------
    # 7. Calculate impact
    # ---------------------------------------------------------

    impact = calculate_impact(
        events,
        diagnosis
    )

    # ---------------------------------------------------------
    # 8. Choose recovery strategy
    # ---------------------------------------------------------

    strategy = choose_recovery_strategy(
        diagnosis
    )

    # ---------------------------------------------------------
    # 9. Choose fallback provider if required
    # ---------------------------------------------------------

    fallback_provider = None

    if strategy == "retry_with_fallback_provider":

        fallback_provider = choose_fallback_provider(
            events,
            diagnosis["value"]
        )

    # ---------------------------------------------------------
    # 10. Identify recovery candidates
    # ---------------------------------------------------------

    candidates = identify_recovery_candidates(
        events,
        diagnosis
    )

    # ---------------------------------------------------------
    # 11. Apply bounded recovery limit
    # ---------------------------------------------------------

    recovery_batch = select_recovery_batch(
        candidates
    )

    # ---------------------------------------------------------
    # 12. Execute recovery
    # ---------------------------------------------------------

    recovery_results = execute_recovery(
        recovery_batch,
        strategy,
        fallback_provider
    )

    # ---------------------------------------------------------
    # 13. Verify recovery
    # ---------------------------------------------------------

    verification = verify_recovery(
        recovery_results
    )

    # ---------------------------------------------------------
    # 14. Create audit record
    # ---------------------------------------------------------

    audit = create_recovery_audit(
        diagnosis,
        strategy,
        fallback_provider,
        recovery_results
    )

    # ---------------------------------------------------------
    # 15. Return complete analysis
    # ---------------------------------------------------------

    return {
        "scenario": scenario,

        "metrics": metrics,

        "anomalies": anomalies,

        "dimension_anomalies": dimension_anomalies,

        "failure_reason_anomalies": failure_reason_anomalies,

        "diagnosis": diagnosis,

        "impact": impact,

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

    # ---------------------------------------------------------
    # Payment Summary
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Incident Diagnosis
    # ---------------------------------------------------------

    print("\nIncident Diagnosis")
    print("------------------")

    diagnosis = result["diagnosis"]

    if diagnosis:

        print(
            f"Type       : "
            f"{diagnosis['type']}"
        )

        print(
            f"Dimension  : "
            f"{diagnosis['dimension']}"
        )

        print(
            f"Value      : "
            f"{diagnosis['value']}"
        )

        print(
            f"Failure    : "
            f"{diagnosis['failure_rate']:.2f}%"
        )

        print(
            f"Baseline   : "
            f"{diagnosis['baseline_failure_rate']:.2f}%"
        )

        print(
            f"Increase   : "
            f"{diagnosis['absolute_increase']:.2f} pp"
        )

        print(
            f"Relative   : "
            f"{diagnosis['relative_increase']:.2f}x"
        )

    else:

        print("No incident diagnosed.")

    # ---------------------------------------------------------
    # Impact Analysis
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Recovery
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Recovery Verification
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Recovery Audit
    # ---------------------------------------------------------

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