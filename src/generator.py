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

def calculate_success_probability(method, bank, provider, timestamp):
    z = (
        INTERCEPT
        + METHOD_EFFECTS[method]
        + BANK_EFFECTS[bank]
        + PROVIDER_EFFECTS[provider]
    )

    if 14 <= timestamp.hour <= 19:
        z += PEAK_HOUR_EFFECT

    return sigmoid(z)    


def generate_payment_event():
    bank=random.choice(list(BANK_EFFECTS.keys()))
    provider=random.choice(list(PROVIDER_EFFECTS.keys()))
    method=random.choice(list(METHOD_EFFECTS.keys()))
    geo=random.choice(GEOGRAPHIES)
    
    start_time=datetime(2026,9,1,9,0,0)

    timestamp=start_time+timedelta(seconds=random.randint(0,50400))

    amount=random.randint(100,10000)
  
    status="failed"
    trans_id=1 #generate unique and random ids
    result=calculate_success_probability(method,bank,provider,timestamp)
    if random.random()<result: ## Sample the payment outcome according to its success probability. 
        status="success"

    if status=="success":
        event=PaymentEvent(trans_id,amount,method,bank,provider,timestamp,geo,status)
    else:
        event=PaymentEvent(trans_id,amount,method,bank,provider,timestamp,geo,status,400) ##random error code for now
    return event    

