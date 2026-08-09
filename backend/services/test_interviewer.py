from data_loader import load_candidates, load_curriculum
from candidate_analyzer import analyze_candidate
from curriculum_mapper import map_candidate_topics
from question_planner import build_interview_plan
from llm_client import generate_interviewer_response


candidates = load_candidates()
curriculum = load_curriculum()

candidate = candidates["candidates"][0]

profile = analyze_candidate(candidate)

mapped_topics = map_candidate_topics(
    profile,
    curriculum
)

plan = build_interview_plan(
    profile,
    mapped_topics
)

current_topic = plan[0]

conversation_history = []


question = generate_interviewer_response(
    profile,
    current_topic,
    conversation_history
)

print("\n===== AI INTERVIEWER =====\n")
print(question)

