def aggregate_events(events):
    if events:
        total_transactions=0
        successful_transactions=0
        failed_transactions=0
        success_rate=0
        failure_rate=0
        total_amount=0
        failed_amount=0

        for event in events:
            if event.status=="success":
                successful_transactions+=1
            elif event.status=="failed":
                failed_transactions+=1
                failed_amount+=event.amount.
            else:
                raise ValueError(f"Unknown payment status: {event.status}")
            total_transactions+=1
            total_amount+=event.amount
        success_rate=(successful_transactions/total_transactions)*100
        failure_rate=(failed_transactions/total_transactions)*100
        
        return {
                "total_transactions": total_transactions,
            "successful_transactions":successful_transactions,
            "failed_transactions":failed_transactions,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "total_amount": total_amount,
            "failed_amount":failed_amount
            }
    return {
    "total_transactions": 0,
    "successful_transactions": 0,
    "failed_transactions": 0,
    "success_rate": 0,
    "failure_rate": 0,
    "total_amount": 0,
    "failed_amount": 0}