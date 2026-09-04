from generator import generate_events
from aggregate import aggregate_events
from datetime import datetime
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

events=generate_events(10000)

metrics=aggregate_events(events)

failed_events = [
    event for event in events
    if event.status == "failed"
]

provider_z_events = [
    event for event in events
    if event.provider == "provider_z"
]

incident_events = [
    event for event in provider_z_events
    if (
        event.timestamp >= datetime(2026, 9, 3, 10, 30)
        and event.timestamp < datetime(2026, 9, 3, 11, 30)
    )
]
print("\nProvider Z Incident Check")
print("-------------------------")

print("First event:", events[0].timestamp)
print("Last event :", events[-1].timestamp)
print("Incident   : 10:30 - 11:30")

print("\nProvider Z Incident Check")
print("-------------------------")

print(f"Provider Z transactions during incident: {len(incident_events)}")

if incident_events:
    incident_failures = [
        event for event in incident_events
        if event.status == "failed"
    ]

    print(f"Failures during incident: {len(incident_failures)}")
    print(
        f"Failure rate during incident: "
        f"{len(incident_failures) / len(incident_events) * 100:.2f}%"
    )

print("Payment Summary")
print("----------------")
print(f"Total transactions : {metrics['total_transactions']}")
print(f"Successful         : {metrics['successful_transactions']}")
print(f"Failed             : {metrics['failed_transactions']}")
print(f"Success rate       : {metrics['success_rate']:.2f}%")
print(f"Failure rate       : {metrics['failure_rate']:.2f}%")
print(f"Total amount       : ₹{metrics['total_amount']}")
print(f"Failed amount      : ₹{metrics['failed_amount']}")

anomalies = detect_anomalies(events)

print("\nSystem-wide Anomalies")
print("---------------------")

if not anomalies:
    print("None")
else:
    for anomaly in anomalies:
        print(
            f"{anomaly['start']} → {anomaly['end']} | "
            f"failure rate: {anomaly['failure_rate']:.2f}% | "
            f"baseline: {anomaly['baseline_failure_rate']:.2f}%"
        )

print("\nProvider Anomalies")
print("------------------")

provider_anomalies = detect_dimension_anomalies_by_window(
    events,
    dimension="provider"
)

if not provider_anomalies:
    print("None")
else:
    for anomaly in provider_anomalies:
        print(
            f"{anomaly['start']} → {anomaly['end']} | "
            f"{anomaly['value']} | "
            f"failure rate: {anomaly['failure_rate']:.2f}% | "
            f"baseline: {anomaly['baseline_failure_rate']:.2f}% | "
            f"increase: {anomaly['absolute_increase']:.2f} pp | "
            f"relative: {anomaly['relative_increase']:.2f}x | "
            f"transactions: {anomaly['transaction_count']}"
        )

# print("\nDetected Anomalies")
# print("------------------")

# for anomaly in anomalies:
#     print(
#         f"{anomaly['start']} → {anomaly['end']} | "
#         f"failure rate: {anomaly['failure_rate']:.2f}% | "
#         f"baseline: {anomaly['baseline_failure_rate']:.2f}% | "
#         f"transactions: {anomaly['transaction_count']}"
#     )

# provider_anomalies = detect_dimension_anomalies_by_window(
#     events,
#     dimension="provider"
# )

# print("\nProvider Anomalies")
# print("------------------")

# for anomaly in provider_anomalies:
#     print(
#         f"{anomaly['start']} → {anomaly['end']} | "
#         f"{anomaly['value']} | "
#         f"failure rate: {anomaly['failure_rate']:.2f}% | "
#         f"baseline: {anomaly['baseline_failure_rate']:.2f}% | "
#         f"increase: {anomaly['absolute_increase']:.2f} pp | "
#         f"relative: {anomaly['relative_increase']:.2f}x | "
#         f"transactions: {anomaly['transaction_count']}"
#     )

diagnosis = diagnose_incident(provider_anomalies)

print("\nIncident Diagnosis")
print("------------------")

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


impact = calculate_impact(events, diagnosis)

print("\nImpact Analysis")
print("----------------")

if impact:
    print(f"Affected transactions : {impact['affected_transactions']}")
    print(f"Failed transactions   : {impact['failed_transactions']}")
    print(f"Payment value at risk : ₹{impact['failed_amount']}")
else:
    print("No impact calculated.")


fallback_provider = choose_fallback_provider(
    events,
    diagnosis["value"]
)

print("\nRecovery Decision")
print("-----------------")
print(f"Degraded provider : {diagnosis['value']}")
print(f"Fallback provider : {fallback_provider}")    

candidates = identify_recovery_candidates(events, diagnosis)

recovery_batch = select_recovery_batch(candidates)

print(f"Recovery candidates : {len(candidates)}")
print(f"Selected for retry  : {len(recovery_batch)}")

recovery_results = execute_recovery(
    recovery_batch,
    fallback_provider
)

recovered = [
    result
    for result in recovery_results
    if result["status"] == "recovered"
]

recovered_amount = sum(
    result["amount"]
    for result in recovered
)

print("\nRecovery Execution")
print("------------------")
print(f"Retry attempts    : {len(recovery_results)}")
print(f"Recovered payments: {len(recovered)}")
print(f"Recovered value   : ₹{recovered_amount}")

verification = verify_recovery(recovery_results)

print("\nRecovery Verification")
print("---------------------")
print(f"Attempts         : {verification['attempted']}")
print(f"Recovered        : {verification['recovered']}")
print(f"Recovery rate    : {verification['recovery_rate']:.2f}%")
print(f"Recovered value  : ₹{verification['recovered_amount']}")


audit = create_recovery_audit(
    diagnosis,
    fallback_provider,
    recovery_results
)

print("\nRecovery Audit")
print("--------------")
print(f"Action           : {audit['action']}")
print(f"Original provider: {audit['original_provider']}")
print(f"Fallback provider: {audit['fallback_provider']}")
print(f"Retry attempts   : {audit['retry_attempts']}")
print(f"Recovered        : {audit['recovered_transactions']}")
print(f"Recovered value  : ₹{audit['recovered_amount']}") 