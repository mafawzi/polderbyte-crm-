import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"

QUALIFICATION_CRITERIA = ["budget", "authority", "need", "timeline"]


def summarize_activity(content: str) -> str:
    """Summarize a single activity note into a short brief."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                "Summarize this sales activity note in 2-3 concise sentences. "
                "Focus on outcomes, commitments, and next steps. "
                "Return plain text only, no preamble.\n\n"
                f"Note: {content}"
            )
        }]
    )
    return resp.content[0].text.strip()


def summarize_deal(deal_title: str, activity_notes: list[str]) -> str:
    """Roll up all activities for a deal into a single brief."""
    joined = "\n---\n".join(activity_notes) if activity_notes else "No activity logged yet."
    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": (
                f"Deal: {deal_title}\n\n"
                f"Activity history:\n{joined}\n\n"
                "Write a short deal brief (3-5 sentences) covering: current status, "
                "key stakeholder sentiment, risks, and the single most important next step. "
                "Plain text only, no preamble, no headers."
            )
        }]
    )
    return resp.content[0].text.strip()


def suggest_next_steps(deal_title: str, activity_notes: list[str]) -> str:
    joined = "\n---\n".join(activity_notes) if activity_notes else "No activity logged yet."
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                f"Deal: {deal_title}\n\nActivity history:\n{joined}\n\n"
                "Suggest the top 3 next actions the sales rep should take, as a short numbered list. "
                "Be specific and actionable."
            )
        }]
    )
    return resp.content[0].text.strip()


def qualify_deal(deal_title: str, activity_notes: list[str]) -> list[dict]:
    """
    Ask Claude to assess BANT criteria from activity history.
    Returns a list of dicts: [{criterion, confirmed, notes, score}, ...]
    """
    joined = "\n---\n".join(activity_notes) if activity_notes else "No activity logged yet."
    prompt = (
        f"Deal: {deal_title}\n\nActivity history:\n{joined}\n\n"
        "Assess this deal against BANT qualification criteria: budget, authority, need, timeline.\n"
        "For each criterion, decide if it is confirmed (true/false) based on the evidence, "
        "give a 0-100 confidence score, and a one-sentence justification.\n"
        "Respond ONLY with valid JSON, no markdown fences, in this exact shape:\n"
        '[{"criterion": "budget", "confirmed": true, "score": 80, "notes": "..."}, ...]\n'
        "Include all 4 criteria even if unconfirmed (score 0, confirmed false, notes explaining why)."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.content[0].text.strip()
    # Guard against accidental markdown fences
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return unqualified criteria rather than crashing the endpoint
        return [{"criterion": c, "confirmed": False, "score": 0, "notes": "AI response could not be parsed"} for c in QUALIFICATION_CRITERIA]
