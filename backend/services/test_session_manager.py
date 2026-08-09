from session_manager import (
    create_session,
    get_session,
    record_answer,
    record_follow_up,
    advance_question,
    get_current_topic
)


candidate = {
    "name": "Test Candidate"
}

plan = [
    {
        "day": 7,
        "topic": "Embeddings",
        "difficulty": "advanced"
    },
    {
        "day": 10,
        "topic": "Retrieval",
        "difficulty": "advanced"
    },
    {
        "day": 23,
        "topic": "MCP",
        "difficulty": "advanced"
    }
]


session = create_session(
    "test-session",
    candidate,
    plan
)

print("Session created:")
print(session["session_id"])

print("\nCurrent topic:")
print(get_current_topic("test-session"))

record_answer(
    "test-session",
    "Explain embeddings.",
    "Embeddings convert information into vectors."
)

record_follow_up(
    "test-session",
    "How would you evaluate embedding quality?"
)

advance_question("test-session")

print("\nAfter first question:")

session = get_session("test-session")

print("Question index:", session["current_question_index"])
print("Answers:", len(session["answers"]))
print("Follow-ups:", len(session["follow_ups"]))

print("\nNext topic:")
print(get_current_topic("test-session"))

