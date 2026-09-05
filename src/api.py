from fastapi import FastAPI
from main import run_recovery_analysis


app = FastAPI(
    title="Payment Recovery Intelligence",
    description="AI-powered payment degradation detection and revenue recovery system",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Payment Recovery Intelligence"
    }


@app.post("/analyze")
def analyze_payments(
    scenario: str = "provider_degradation"
):
    """
    Run the payment recovery analysis for the selected scenario.
    """

    return run_recovery_analysis(
        scenario=scenario
    )