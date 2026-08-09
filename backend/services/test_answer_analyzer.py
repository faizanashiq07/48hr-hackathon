from data_loader import load_candidates, load_curriculum
from candidate_analyzer import analyze_candidate
from curriculum_mapper import map_candidate_topics
from question_planner import build_interview_plan
from answer_analyzer import analyze_answer


# Load data
candidates = load_candidates()
curriculum = load_curriculum()

# Use the first supplied candidate
candidate = candidates["candidates"][0]

# Analyze candidate
profile = analyze_candidate(candidate)

# Map candidate topics
mapped_topics = map_candidate_topics(
    profile,
    curriculum
)

# Build interview plan
plan = build_interview_plan(
    profile,
    mapped_topics
)

# Use the first planned topic
current_topic = plan[0]

# Example interviewer question
question = (
    f"Suppose you are building a production system involving "
    f"{current_topic['topic']}. "
    f"How would you approach the main engineering challenge "
    f"associated with this topic?"
)

# Simulated candidate answer
answer = """
I would first understand the requirements and identify the
main components of the system. Then I would choose an
appropriate architecture and evaluate it using relevant
metrics. I would also test the system with different inputs
before deploying it.
"""

conversation_history = []

result = analyze_answer(
    profile,
    current_topic,
    question,
    answer,
    conversation_history
)

print("\n===== ANSWER ANALYSIS =====\n")

print("Assessment:", result["assessment"])
print("Score:", result["score"])

print("\nStrengths:")
for item in result["strengths"]:
    print("-", item)

print("\nMissing concepts:")
for item in result["missing_concepts"]:
    print("-", item)

print("\nFollow-up needed:", result["follow_up_needed"])

print("Follow-up reason:")
print(result["follow_up_reason"])

print("\nSuggested follow-up focus:")
print(result["suggested_follow_up_focus"])

