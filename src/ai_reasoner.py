import json
import os

from google import genai


MODEL_NAME = "gemini-3.7-flash"


def build_recovery_evidence(
    diagnosis,
    impact,
    provider_health,
    recovery_options
):
    """
    Build the structured evidence supplied to the AI reasoner.

    The AI receives observed evidence and available actions.
    It does not calculate the underlying metrics itself.
    """
    return {
        "diagnosis": diagnosis,
        "impact": impact,
        "provider_health": provider_health,
        "available_recovery_options": recovery_options
    }


def reason_about_recovery(
    diagnosis,
    impact,
    provider_health,
    recovery_options
):
    """
    Ask Gemini to recommend the safest recovery action
    based on the evidence produced by the deterministic pipeline.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    evidence = build_recovery_evidence(
        diagnosis=diagnosis,
        impact=impact,
        provider_health=provider_health,
        recovery_options=recovery_options
    )

    prompt = f"""
You are the recovery reasoning component of a payment revenue
recovery system.

Your job is to recommend the safest available recovery action
based ONLY on the supplied evidence.

You must NOT invent facts.

You must NOT execute any payment action.

You must choose ONLY from the available recovery options.

The deterministic system will enforce final safety guardrails
after your recommendation.

Evidence:

{json.dumps(evidence, indent=2, default=str)}

Evaluate:

1. What is the most likely recovery action?
2. If a fallback provider is appropriate, which available provider
   appears healthiest?
3. Why is the recommendation appropriate?
4. How confident are you?
5. What is the operational risk?

Return a concise structured recommendation.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": {
                "type": "object",
                "properties": {
                    "recommended_strategy": {
                        "type": "string"
                    },
                    "recommended_provider": {
                        "type": ["string", "null"]
                    },
                    "reasoning": {
                        "type": "string"
                    },
                    "confidence": {
                        "type": "number"
                    },
                    "risk": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ]
                    },
                    "expected_recovery": {
                        "type": "string"
                    }
                },
                "required": [
                    "recommended_strategy",
                    "recommended_provider",
                    "reasoning",
                    "confidence",
                    "risk",
                    "expected_recovery"
                ]
            }
        }
    )

    return json.loads(response.text)