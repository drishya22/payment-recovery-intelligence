import math
import random
import uuid
from datetime import datetime, timedelta
from models import PaymentEvent


METHOD_EFFECTS = {
    "upi": 0.15,
    "credit_card": -0.10,
    "debit_card": 0.05,
    "net_banking": -0.10,
    "wallet": 0.05
}

BANK_EFFECTS = {
    "bank_a": 0.05,
    "bank_b": 0.00,
    "bank_c": -0.05,
    "bank_d": 0.03,
    "bank_e": -0.03,
    "bank_f": 0.02
}

PROVIDER_EFFECTS = {
    "provider_x": 0.03,
    "provider_y": 0.00,
    "provider_z": -0.03
}

GEOGRAPHIES = [
    "delhi_ncr",
    "mumbai",
    "bengaluru",
    "hyderabad",
    "chennai",
    "kolkata",
    "pune"
]

INCIDENTS = {
    "provider_degradation": {
        "type": "provider_degradation",
        "start": datetime(2026, 9, 3, 10, 30, 0),
        "end": datetime(2026, 9, 3, 11, 30, 0),
        "provider": "provider_z"
    },

    "bank_degradation": {
        "type": "bank_degradation",
        "start": datetime(2026, 9, 3, 12, 0, 0),
        "end": datetime(2026, 9, 3, 13, 0, 0),
        "bank": "bank_a"
    },

    "timeout_spike": {
        "type": "timeout_spike",
        "start": datetime(2026, 9, 3, 14, 0, 0),
        "end": datetime(2026, 9, 3, 15, 0, 0)
    }
}

FAILURE_REASONS = {
    "provider_degradation": {
        "reason": "provider_error",
        "error_code": 502
    },
    "bank_degradation": {
        "reason": "bank_technical_error",
        "error_code": 503
    },
    "timeout_spike": {
        "reason": "payment_timeout",
        "error_code": 408
    }
}

INTERCEPT = 3.0
PEAK_HOUR_EFFECT = -0.10

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def calculate_success_probability(method, bank, provider, timestamp, incident=None):
    z = (
        INTERCEPT
        + METHOD_EFFECTS[method]
        + BANK_EFFECTS[bank]
        + PROVIDER_EFFECTS[provider]
    )

    if 14 <= timestamp.hour <= 19:
        z += PEAK_HOUR_EFFECT

    #simulated incident: when provider_z is degraded, its success probability drops significantly
    if incident:
        if (incident["type"]=="provider_degradation" and provider==incident["provider"]):
            z-=2.0
        elif (incident["type"] == "bank_degradation" and bank == incident["bank"]):
            z -= 2.0
        elif incident["type"] == "timeout_spike":
            z -= 1.5
    return sigmoid(z)    


def generate_payment_event(timestamp,trans_id,incident=None):
    """
    Generate one synthetic payment event.

    This function represents the behaviour of a single payment:
    - randomly chooses payment attributes
    - calculates probability of success
    - samples the final payment outcome
    """

    bank=random.choice(list(BANK_EFFECTS.keys()))
    provider=random.choice(list(PROVIDER_EFFECTS.keys()))
    method=random.choice(list(METHOD_EFFECTS.keys()))
    geo=random.choice(GEOGRAPHIES)

    amount=random.randint(100,10000)

    success_probability=calculate_success_probability(method, bank, provider, timestamp,incident)
    # Randomly determine the actual outcome according to
    # the calculated probability.
    if random.random() < success_probability:
        status = "success"
        error_code = None
        failure_reason = None

    else:
        status = "failed"

        affected_by_incident = False

        if incident:
            if (
                incident["type"] == "provider_degradation"
                and provider == incident["provider"]
            ):
                affected_by_incident = True

            elif (
                incident["type"] == "bank_degradation"
                and bank == incident["bank"]
            ):
                affected_by_incident = True

            elif incident["type"] == "timeout_spike":
                affected_by_incident = True

        if affected_by_incident:
            failure = FAILURE_REASONS[incident["type"]]
            failure_reason = failure["reason"]
            error_code = failure["error_code"]

        else:
            failure_reason = "generic_payment_failure"
            error_code = 400


    # Create and return the payment event.
    return PaymentEvent(
        trans_id,
        amount,
        method,
        bank,
        provider,
        timestamp,
        geo,
        status,
        error_code,
        failure_reason,
        incident_type=incident["type"] if incident else None
    )  

def generate_events(num_events,start_time,duration_hours,scenario="provider_degradation"):
    """
    Generate a chronological stream of synthetic payment events.
    num_events: Number of ayment events to generate
    start_time: Beginning of the simulation
    duration_hours: Duration of the simulation.
    Returns: A list of PaymentEvent objects ordered by timestamp
    """

    events=[]
    end_time=start_time+timedelta(hours=duration_hours)

    current_timestamp=start_time

    total_seconds = (
        end_time-start_time
    ).total_seconds()

    target_interval = total_seconds / (num_events - 1)

    for _ in range(1,num_events+1):
        trans_id = str(uuid.uuid4())
        incident=INCIDENTS.get(scenario)
        if not (incident and incident["start"]<=current_timestamp<incident["end"]):
            incident=None
        event=generate_payment_event(
            current_timestamp,
            trans_id,
            incident
        )
        events.append(event)
        time_gap = random.uniform(
            target_interval * 0.5,
            target_interval * 1.5
        )
        current_timestamp+=timedelta(seconds=time_gap)
        if current_timestamp>end_time:
            current_timestamp=end_time

        
    print("Simulation start:", events[0].timestamp)
    print("Simulation end:", events[-1].timestamp)
    return events


if __name__=="__main__":
    events = generate_events(
    num_events=1000,
    start_time=datetime(2026, 9, 3, 9, 0, 0),
    duration_hours=9,
    scenario="bank_degradation")

    for event in events:
        if event.status == "failed":
            print(
                event.timestamp,
                event.provider,
                event.status,
                event.failure_reason,
                event.error_code,
                event.incident_type,
                event.bank
            )