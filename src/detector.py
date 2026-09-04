from datetime import datetime,timedelta

ANALYSIS_DIMENSIONS = [
    "provider",
    "bank",
    "method",
    "geo"
]

def calculate_failure_rate(events):
    if not events:
        return 0.0
    
    failed=sum(1 for event in events if event.status=="failed")
    return (failed/len(events))*100

def filter_events_by_dimension(events, dimension, value):
    """
    Return only the events matching a particular dimension.

    Example:

        dimension = "provider"
        value = "provider_z"

    returns only payments made through provider_z.
    """

    return [
        event
        for event in events
        if getattr(event, dimension) == value
    ]

def create_time_windows(events,window_minutes=60):
    if not events:
        return []
    start_time=events[0].timestamp

    start_time=start_time.replace(
        minute=(start_time.minute//window_minutes)*window_minutes,
        second=0,
        microsecond=0
    )
    windows=[]

    current_start=start_time
    current_end=current_start+timedelta(minutes=window_minutes)

    current_events=[]
    for event in events:
        if event.timestamp<current_end:
            current_events.append(event)
        else:
            windows.append({
                "start":current_start,
                "end": current_end,
                "events" : current_events
            })
            current_start=current_end
            current_end=current_start+timedelta(minutes=window_minutes)
            current_events=[event]
    if current_events:
        windows.append({
            "start": current_start,
            "end" : current_end,
            "events": current_events
        })
    return windows


def detect_anomalies(events,threshold_multiplier=2.0,window_minutes=60):
    """
    Detect time windows where payment failures are
    significantly higher than the baseline.

    threshold_multiplier:
        How many times higher than baseline a window
        must be before we flag it.

        Example:
            baseline=5%
            multiplier=2
            threshold=10%

    Returns:
        A list of anomalous windows.
    """
    if not events:
        return []
    baseline_failure_rate=calculate_failure_rate(events)
    windows=create_time_windows(events,window_minutes)

    anomalies=[]
    for window in windows:
        window_events=window["events"]
        if len(window_events)<10:  #ignore very small windows as they are not statistically useful
            continue
        failure_rate=calculate_failure_rate(window_events)
        
        threshold=baseline_failure_rate*threshold_multiplier
        if failure_rate>threshold:
            anomalies.append({
                "start":window["start"],
                "end":window["end"],
                "failure_rate":failure_rate,
                "baseline_failure_rate": baseline_failure_rate,
                "threshold":threshold,
                "transaction_count":len(window_events)
            })
    return anomalies


def detect_dimension_anomalies(events,dimension,threshold_multiplier=2.0,min_transactions=10):
    """
    Detect whether a particular dimension has an unusually high failure rate.
    Example:
    dimension="provider"
    the function will compare:
    1. provider_x failure rate
    2. provider_y failure rate
    3. provider_z failure rate 

    against the overall baseline
    """

    baseline_failure_rate=calculate_failure_rate(events)
    dimension_values=set(getattr(event,dimension) for event in events)

    anomalies=[]

    for value in dimension_values:
        matching_events=filter_events_by_dimension(events,dimension,value)
        if len(matching_events)<min_transactions:
            continue
        failure_rate=calculate_failure_rate(matching_events)
        threshold=baseline_failure_rate*threshold_multiplier

        if failure_rate>threshold:
            anomalies.append({
                "dimension":dimension,
                "value":value,
                "failure_rate": failure_rate,
                "baseline_failure_rate": baseline_failure_rate,
                "threshold":threshold,
                "transaction_count":len(matching_events)
            })
    return anomalies        


def detect_dimension_anomalies_by_window(events,dimension,threshold_multiplier=2.0,min_absolute_increase=10.0,min_transactions=10,window_minutes=30):
    """
    Detect dimension-specific anomalies inside time windows.

    Each dimension value is compared against its own historical
    failure-rate baseline.

    Example for dimension="provider":

        provider_z baseline  -> 8%
        provider_z current   -> 20%

    The provider is flagged when:

        1. Current failure rate is greater than
           baseline × threshold_multiplier

        AND

        2. Current failure rate exceeds the baseline by at least
           min_absolute_increase percentage points.

    This combination reduces false positives caused by
    small proportional changes in low-failure-rate dimensions.

    """

    if not events:
        return []
    
    windows=create_time_windows(events,window_minutes)
    dimension_values=set(getattr(event,dimension) for event in events)

    baselines={}
    for value in dimension_values:
        matching_events=filter_events_by_dimension(events,dimension,value)
        if len(matching_events)>=min_transactions:
            baselines[value]=calculate_failure_rate(matching_events)
    
    anomalies=[]
    for window in windows:
        window_events=window["events"]
        if len(window_events)<min_transactions:
            continue
        for value,baseline_failure_rate in baselines.items():
            dimensions_events=filter_events_by_dimension(window_events,dimension,value)

            if len(dimensions_events)<min_transactions:
                continue
            window_failure_rate=calculate_failure_rate(dimensions_events)
            relative_threshold=baseline_failure_rate*threshold_multiplier
            absolute_increase=window_failure_rate-baseline_failure_rate
            if window_failure_rate>relative_threshold and absolute_increase>=min_absolute_increase:
                anomalies.append({
                    "start":window["start"],
                    "end":window["end"],
                    "dimension":dimension,
                    "value":value,
                    "failure_rate":window_failure_rate,
                    "baseline_failure_rate":baseline_failure_rate,
                    "threshold":relative_threshold,
                    "relative_increase": (
                        window_failure_rate / baseline_failure_rate
                        if baseline_failure_rate > 0
                        else float("inf")
                    ),
                    "absolute_increase": absolute_increase,
                    "transaction_count": len(dimensions_events)
                })
    return anomalies
