import json
import os

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------
# GROQ SETUP
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


# ---------------------------------------------------------
# ANSWER ANALYZER
# ---------------------------------------------------------

def analyze_answer(
    candidate_profile,
    current_topic,
    question,
    answer,
    conversation_history
):
    """
    Evaluate ONE candidate answer.

    IMPORTANT:
    This function intentionally sends only compact information
    to Groq so the request stays well below the TPM limit.
    """

    # -----------------------------------------------------
    # Keep candidate information minimal
    # -----------------------------------------------------

    candidate_name = candidate_profile.get(
        "name",
        "Candidate"
    )

    candidate_role = candidate_profile.get(
        "job_role",
        "AI Engineer"
    )

    # -----------------------------------------------------
    # Keep curriculum information minimal
    # -----------------------------------------------------

    day = current_topic.get(
        "day",
        "Unknown"
    )

    topic = current_topic.get(
        "topic",
        "Unknown"
    )

    difficulty = current_topic.get(
        "difficulty",
        "intermediate"
    )

    objectives = current_topic.get(
        "objectives",
        []
    )

    # Only keep a few objectives.
    objectives = objectives[:3]

    # -----------------------------------------------------
    # DO NOT send the entire conversation history.
    #
    # We only need a tiny amount of recent context.
    # -----------------------------------------------------

    recent_context = []

    if conversation_history:

        for item in conversation_history[-2:]:

            if isinstance(item, dict):

                recent_context.append(
                    {
                        "question": str(
                            item.get("question", "")
                        )[:500],

                        "answer": str(
                            item.get("answer", "")
                        )[:700]
                    }
                )

    # -----------------------------------------------------
    # Limit the current answer too.
    #
    # This protects us from accidentally sending enormous
    # answers to the model.
    # -----------------------------------------------------

    answer = str(answer)[:4000]

    question = str(question)[:2500]

    # -----------------------------------------------------
    # SYSTEM PROMPT
    # -----------------------------------------------------

    system_prompt = """
You are a senior technical interviewer evaluating one
candidate answer.

Evaluate only the current question.

Assess:

1. Technical correctness
2. Depth of understanding
3. Reasoning
4. Relevance
5. Practical application

Use the supplied curriculum objectives as the evaluation basis.

Do not invent information about the candidate.

Decide whether ONE targeted follow-up question would help
test an unclear or shallow part of the answer.

Return ONLY valid JSON.

Required JSON:

{
  "assessment": "strong | adequate | weak",
  "score": 0,
  "strengths": [],
  "missing_concepts": [],
  "follow_up_needed": true,
  "follow_up_reason": "",
  "suggested_follow_up_focus": ""
}

Score:

0-3 = weak
4-6 = adequate
7-8 = strong
9-10 = excellent

If no follow-up is needed, use:

"follow_up_needed": false,
"follow_up_reason": "",
"suggested_follow_up_focus": ""

Keep the response concise.
"""

    # -----------------------------------------------------
    # USER PROMPT
    # -----------------------------------------------------

    user_prompt = f"""
Candidate: {candidate_name}
Role: {candidate_role}

Current topic:
Day {day} - {topic}

Difficulty:
{difficulty}

Curriculum objectives:
{json.dumps(objectives)}

Question:
{question}

Candidate answer:
{answer}

Recent context:
{json.dumps(recent_context)}

Evaluate this answer.
Return ONLY the required JSON.
"""

    # -----------------------------------------------------
    # GROQ CALL
    # -----------------------------------------------------

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
        temperature=0.1,
        max_completion_tokens=300
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty answer analysis."
        )

    content = content.strip()

    # -----------------------------------------------------
    # Remove markdown fences if returned
    # -----------------------------------------------------

    if content.startswith("```"):

        content = content.replace(
            "```json",
            "",
            1
        )

        content = content.replace(
            "```",
            "",
            1
        )

        content = content.strip()

    # -----------------------------------------------------
    # Parse JSON
    # -----------------------------------------------------

    try:

        result = json.loads(content)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "Groq returned invalid JSON:\n"
            + content
        ) from error

    return result

