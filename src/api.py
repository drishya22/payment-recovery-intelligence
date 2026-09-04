from fastapi import FastAPI
from main import run_recovery_analysis

app=FastAPI(
    title="Payment Recovery Intelligence",
    description="AI-powered payment degradation deection and revenue recovery system",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {
        "status":"online",
        "service":"Payment Recovery Intelligence"
    }

@app.post("/analyze")
def analyze_payment():
    return run_recovery_analysis() 
