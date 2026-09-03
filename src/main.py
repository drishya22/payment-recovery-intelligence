from generator import generate_events
from aggregate import aggregate_events
from datetime import datetime
from detector import detect_anomalies, detect_dimension_anomalies_by_window

events=generate_events(1000)

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