from data_loader import load_candidates
from interview_controller import (
    start_interview,
    process_answer,
)


# Load supplied candidates
data = load_candidates()

candidate = data["candidates"][0]

session_id = "controller-test-001"


print("\n===== STARTING INTERVIEW =====\n")

result = start_interview(
    session_id,
    candidate
)

print("INTERVIEWER:")
print(result["reply"])

print("\nDONE:", result["done"])


# Simulate candidate answer
answer = """
I would first identify the requirements and then design the
architecture around the expected workload. I would evaluate
the system using appropriate metrics and test it with
representative examples.
"""


print("\n===== CANDIDATE ANSWER =====\n")
print(answer)


result = process_answer(
    session_id,
    answer
)


print("\n===== NEXT INTERVIEWER RESPONSE =====\n")
print(result["reply"])

print("\nDONE:", result["done"])

