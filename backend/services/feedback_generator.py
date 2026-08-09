import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not configured")


client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


def generate_feedback(candidate_profile, evaluations):
    """
    Generate structured final interview feedback from
    the candidate's complete interview evaluations.
    """

    system_prompt = """
You are a senior technical interviewer preparing final
feedback for a candidate after a technical interview.

Your feedback must be:

- evidence-based
- concise
- actionable
- specific to the candidate's answers
- grounded in the supplied curriculum topics

Do not invent achievements or weaknesses.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
    "summary": "string",
    "strengths": ["string"],
    "gaps": ["string"],
    "recommendations": ["string"]
}

Rules:

1. Summary should give an overall assessment.
2. Strengths should identify demonstrated technical abilities.
3. Gaps should identify concepts that need improvement.
4. Recommendations should give concrete next steps.
5. Base every point on the supplied interview evidence.
6. Do not mention internal scoring mechanics.
7. Do not include markdown.
"""

    user_prompt = f"""
CANDIDATE

Name:
{candidate_profile.get("name")}

Role:
{candidate_profile.get("job_role")}

Experience:
{candidate_profile.get("years_experience")} years


INTERVIEW EVALUATIONS

{json.dumps(evaluations, indent=2)}


Generate the final structured feedback.

Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=700
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty feedback response."
        )

    content = content.strip()

    # Remove accidental markdown fences.
    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Groq returned invalid feedback JSON:\n{content}"
        ) from error

    return result

