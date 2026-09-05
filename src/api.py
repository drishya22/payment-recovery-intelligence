from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main import run_recovery_analysis


app = FastAPI(
    title="Payment Recovery Intelligence",
    description="AI-powered payment degradation detection and revenue recovery system",
    version="1.0.0"
)


# Allow the React dashboard to communicate with the API.
# The frontend and backend run on different Codespaces ports,
# so the browser treats them as different origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jubilant-space-chainsaw-69gxq95wjwpp3rv7g-5173.app.github.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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