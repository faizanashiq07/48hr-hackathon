import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not configured")


# Create Groq client
client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


def generate_interviewer_response(
    candidate_profile,
    current_topic,
    conversation_history
):
    system_prompt = """
You are a senior technical interviewer conducting a realistic
technical interview for an AI engineering cohort.

Your job is to evaluate the candidate's technical understanding,
reasoning ability, and engineering judgment.

STRICT RULES:

1. Ask EXACTLY ONE question in each response.

2. Never combine multiple independent questions.

3. A scenario is allowed, but it must lead to one clear question.

4. Focus ONLY on the current curriculum topic.

5. Use the curriculum objectives to determine what knowledge to test.

6. Personalize the difficulty using the candidate's experience
   and learning history.

7. If the candidate gives a strong answer, probe deeper.

8. If the candidate gives a weak or incomplete answer, probe the
   missing concept.

9. Do not reveal the correct answer.

10. Do not teach or lecture before the candidate answers.

11. Do not repeat questions already asked.

12. Prefer realistic engineering scenarios over simple definitions.

13. Do not introduce unrelated technologies or domains.

14. Keep the response concise.

15. Return ONLY the message the interviewer should say.
"""

    user_prompt = f"""
CANDIDATE

Name: {candidate_profile.get("name")}
Role: {candidate_profile.get("job_role")}
Experience: {candidate_profile.get("years_experience")} years

Strong areas:
{candidate_profile.get("strong_areas", [])}

Weak areas:
{candidate_profile.get("weak_areas", [])}

Skipped areas:
{candidate_profile.get("skipped_areas", [])}

High-effort areas:
{candidate_profile.get("high_effort_areas", [])}


CURRENT CURRICULUM TOPIC

Day: {current_topic.get("day")}

Topic: {current_topic.get("topic")}

Difficulty: {current_topic.get("difficulty")}

Reason:
{current_topic.get("reason")}

Objectives:
{current_topic.get("objectives", [])}


PREVIOUS CONVERSATION

{conversation_history}


TASK

Generate exactly ONE focused technical interview question.

The question must:

- focus on the current topic
- reflect the curriculum objectives
- match the candidate's experience
- require reasoning or technical explanation
- use previous conversation context when available
- not repeat a previous question

Return ONLY the interviewer's message.
Do not provide an answer.
Do not provide feedback.
Do not ask multiple questions.
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
        temperature=0.4,
        max_completion_tokens=800
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty interviewer response."
        )

    return content.strip()

