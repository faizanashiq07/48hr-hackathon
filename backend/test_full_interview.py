import requests
import json


API_URL = "http://127.0.0.1:8000/api/interview"

MEMBER_ID = "CAND-001"


def start_interview():
    response = requests.post(
        API_URL,
        json={
            "memberId": MEMBER_ID
        }
    )

    response.raise_for_status()

    return response.json()


def answer_interview(session_id, answer):
    response = requests.post(
        API_URL,
        json={
            "memberId": MEMBER_ID,
            "sessionId": session_id,
            "message": answer
        }
    )

    response.raise_for_status()

    return response.json()


print("\n========================================")
print("       FULL AI INTERVIEW TEST")
print("========================================\n")


# ---------------------------------------------------------
# START
# ---------------------------------------------------------

result = start_interview()

session_id = result["sessionId"]

question_count = 1

print(f"QUESTION {question_count}")
print("----------------------------------------")
print(result["reply"])
print()


# ---------------------------------------------------------
# GENERIC CANDIDATE ANSWER
# ---------------------------------------------------------

answer = """
I would first clarify the requirements and understand the
expected system behavior. Then I would choose an appropriate
architecture based on scalability, reliability and latency.

I would validate the design using representative test cases
and monitor the system using suitable evaluation metrics.
"""


# ---------------------------------------------------------
# CONTINUE INTERVIEW
# ---------------------------------------------------------

max_turns = 18

for turn in range(max_turns):

    result = answer_interview(
        session_id,
        answer
    )

    if result["done"]:

        print("========================================")
        print("INTERVIEW FINISHED")
        print("========================================\n")

        print("FINAL RESPONSE:")
        print(result["reply"])

        print("\nFINAL FEEDBACK:")

        print(
            json.dumps(
                result.get("feedback"),
                indent=2
            )
        )

        print("\nTotal questions:", question_count)

        break

    question_count += 1

    print(f"QUESTION {question_count}")
    print("----------------------------------------")
    print(result["reply"])
    print()

else:

    print("========================================")
    print("TEST STOPPED")
    print("========================================")

    print(
        f"The interview did not finish within "
        f"{max_turns} turns."
    )