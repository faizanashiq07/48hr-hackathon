from data_loader import load_candidates, load_curriculum
from candidate_analyzer import analyze_candidate
from curriculum_mapper import map_candidate_topics
from question_planner import build_interview_plan
from answer_analyzer import analyze_answer
from follow_up_generator import generate_follow_up


# Load data
candidates = load_candidates()
curriculum = load_curriculum()

# Select candidate
candidate = candidates["candidates"][0]

# Analyze candidate
profile = analyze_candidate(candidate)

# Map curriculum topics
mapped_topics = map_candidate_topics(
    profile,
    curriculum
)

# Build interview plan
plan = build_interview_plan(
    profile,
    mapped_topics
)

current_topic = plan[0]


# Initial question
question = (
    f"Suppose you are building a production system involving "
    f"{current_topic['topic']}. "
    f"How would you approach the main engineering challenge "
    f"associated with this topic?"
)


# Simulated weak/general answer
answer = """
I would first understand the requirements and then choose
an appropriate architecture. After implementing it, I would
test the system and monitor its performance.
"""


conversation_history = []


# Analyze the answer
analysis = analyze_answer(
    profile,
    current_topic,
    question,
    answer,
    conversation_history
)


print("\n===== ANSWER ANALYSIS =====\n")
print(analysis)


# Generate follow-up only if needed
if analysis["follow_up_needed"]:

    follow_up = generate_follow_up(
        profile,
        current_topic,
        question,
        answer,
        analysis,
        conversation_history
    )

    print("\n===== ADAPTIVE FOLLOW-UP =====\n")
    print(follow_up)

else:

    print("\nNo follow-up needed.")

