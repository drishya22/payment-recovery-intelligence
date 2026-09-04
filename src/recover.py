import random


def identify_recovery_candidates(events,diagnosis):
    """
    Identify failed payments that are eligible for recovery.
    """
    if not diagnosis:
        return []
    
    candidates=[
        event
        for event in events
        if (
            diagnosis["start"]<=event.timestamp<diagnosis["end"] and getattr(event,diagnosis["dimension"])==diagnosis["value"]
            and event.status=="failed"
        )
    ]
    return candidates

def choose_fallback_provider(events,degraded_provider):
    provider_stats=dict()
    for event in events:
        if event.provider==degraded_provider:
            continue
        if event.provider not in provider_stats:
            provider_stats[event.provider]={
                "total":0,
                "failed":0
            }
        provider_stats[event.provider]["total"]+=1
        if event.status=="failed":
            provider_stats[event.provider]["failed"]+=1
    if not provider_stats:
        return None
    return min(
        provider_stats, key=lambda provider: provider_stats[provider]["failed"]/provider_stats[provider]["total"]
    )     

def select_recovery_batch(candidates, max_retries=100):
    """
    Select a bounded batch of failed payments for recovery. 
    The retry limit prevents the recovery system from attempting an unbounded number of payments.
    """
    return candidates[:max_retries]   


def execute_recovery(recovery_batch,fallback_provider):
    if not recovery_batch or not fallback_provider:
        return []
    results=[]
    for event in recovery_batch:

        recovered=random.random()<0.90

        results.append({
            "transaction_id": event.id,
            "amount":event.amount,
            "original_provider":event.provider,
            "fallback_provider":fallback_provider,
            "status": "recovered" if recovered else "failed"
        })             
    return results


def verify_recovery(recovery_results):
    if not recovery_results:
        return {
            "attempted":0,
            "recovered":0,
            "recovered_amount":0,
            "recovery_rate":0.0
        }      

    recovered=[
        result
        for result in recovery_results
        if result["status"]=="recovered"
    ]   

    recovered_amount=sum(result["amount"] for result in recovered)   


    return {
        "attempted": len(recovery_results),
        "recovered": len(recovered),
        "recovered_amount": recovered_amount,
        "recovery_rate": len(recovered)/len(recovery_results)*100
    }

def create_recovery_audit(diagnosis,fallback_provider,recovery_results):
    """
    Create an audit record describing the recovery action.
    """

    recovered=[
        result 
        for result in recovery_results
        if result["status"]=="recovered"
    ]
    recovered_amount=sum(result["amount"] for result in recovered)


    return {
        "incident_type":diagnosis["type"],
        "affected_dimension": diagnosis["dimension"],
        "affected_value":diagnosis["value"],
        "incident_start":diagnosis["start"],
        "incident_end":diagnosis["end"],
        "original_provider":diagnosis["value"],
        "fallback_provider":fallback_provider,
        "retry_attempts":len(recovery_results),
        "recovered_transactions": len(recovered),
        "recovered_amount": recovered_amount,
        "action": "retry_with_fallback_provider"
    }    