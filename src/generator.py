import math
import random
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

INTERCEPT = 3.0
PEAK_HOUR_EFFECT = -0.10


def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def calculate_success_probability(method, bank, provider, timestamp, provider_z_degraded=False):
    z = (
        INTERCEPT
        + METHOD_EFFECTS[method]
        + BANK_EFFECTS[bank]
        + PROVIDER_EFFECTS[provider]
    )

    if 14 <= timestamp.hour <= 19:
        z += PEAK_HOUR_EFFECT

    #simulated incident: when provider_z is degraded, its success probability drops significantly
    if provider_z_degraded and provider=="provider_z":
        z-=2.0

    return sigmoid(z)    


def generate_payment_event(timestamp,trans_id,provider_z_degraded=False):
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

    success_probability=calculate_success_probability(method, bank, provider, timestamp, provider_z_degraded)
    # Randomly determine the actual outcome according to
    # the calculated probability.
    if random.random() < success_probability:
        status = "success"
        error_code = None
    else:
        status = "failed"
        error_code = 400       # Temporary generic failure code.


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
        error_code
    )  

def generate_events(num_events):
    """
    Generate a chronological stream of synthetic payment events.
    num_events: Number of ayment events to generate
    Returns: A list of PaymentEvent objects ordered by timestamp
    """

    events=[]

    current_timestamp=datetime(2026,9,3,9,0,0)
    incident_start=datetime(2026,9,3,10,30,0)
    incident_end=datetime(2026,9,3,11,30,0)

    for trans_id in range(1,num_events+1):
        provider_z_degraded=(incident_start<=current_timestamp<incident_end)
        event=generate_payment_event(
            current_timestamp,
            trans_id,
            provider_z_degraded
        )
        events.append(event)
        time_gap=random.randint(1,60)
        current_timestamp+=timedelta(seconds=time_gap)

        
    print("Simulation start:", events[0].timestamp)
    print("Simulation end:", events[-1].timestamp)
    return events


if __name__=="__main__":
    events=generate_events(10)
    for event in events:
        print(event.id,event.timestamp,event.method,event.bank,event.provider,event.status)    