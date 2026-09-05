class PaymentEvent:
    def __init__(self,trans_id,amount,method,bank,provider,timestamp,geo,status,error_code=None,failure_reason=None,incident_type=None):
        self.id=trans_id
        self.amount=amount
        self.method=method
        self.bank=bank
        self.provider=provider
        self.geo=geo
        self.timestamp=timestamp
        self.status=status
        self.error_code=error_code
        self.failure_reason=failure_reason
        self.incident_type=incident_type