def calculate_impact(events,diagnosis):
    """
    Calculate the payment value affected by a diagnosis incident. 
    Returns:
    A structured impact summary.
    """

    if not diagnosis:
        return None
    
    affected_events=[
        event 
        for event in events 
        if (diagnosis["start"]<=event.timestamp<diagnosis["end"] and getattr(event,diagnosis["dimension"])==diagnosis["value"])
    ]

    failed_events=[
        event
        for event in affected_events
        if event.status=="failed"
    ]

    failed_amount=sum(event.amount for event in failed_events)

    return {
        "affected_transactions": len(affected_events),
        "failed_transactions":len(failed_events),
        "failed_amount":failed_amount

    }