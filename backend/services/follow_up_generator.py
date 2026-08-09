import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not configured")


client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


def generate_follow_up(
    candidate_profile,
    current_topic,
    previous_question,
    candidate_answer,
    analysis,
    conversation_history
):
    """
    Generate one targeted follow-up question based on
    the candidate's previous answer.
    """

    system_prompt = """
You are a senior technical interviewer.

Generate ONE concise follow-up question based specifically
on the candidate's previous answer.

The follow-up must:

1. Focus on the current curriculum topic.
2. Address the specific missing or unclear concept identified
   by the answer analysis.
3. Build naturally on the candidate's previous answer.
4. Require technical reasoning.
5. Ask exactly ONE question.
6. Never reveal the correct answer.
7. Never lecture or provide feedback.
8. Never introduce an unrelated topic.
9. Do not repeat the previous question.
10. Return ONLY the interviewer's question.
"""

    user_prompt = f"""
CANDIDATE

Name:
{candidate_profile.get("name")}

Role:
{candidate_profile.get("job_role")}

Experience:
{candidate_profile.get("years_experience")} years


CURRENT TOPIC

Day:
{current_topic.get("day")}

Topic:
{current_topic.get("topic")}

Objectives:
{current_topic.get("objectives", [])}


PREVIOUS QUESTION

{previous_question}


CANDIDATE ANSWER

{candidate_answer}


ANSWER ANALYSIS

Assessment:
{analysis.get("assessment")}

Score:
{analysis.get("score")}

Strengths:
{analysis.get("strengths", [])}

Missing concepts:
{analysis.get("missing_concepts", [])}

Follow-up reason:
{analysis.get("follow_up_reason")}

Suggested follow-up focus:
{analysis.get("suggested_follow_up_focus")}


CONVERSATION HISTORY

{conversation_history}


TASK

Generate exactly ONE targeted follow-up question.

Return ONLY the question.
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
        temperature=0.3,
        max_completion_tokens=400
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty follow-up question."
        )

    return content.strip()

