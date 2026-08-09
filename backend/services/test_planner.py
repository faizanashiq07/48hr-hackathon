from data_loader import load_candidates, load_curriculum
from candidate_analyzer import analyze_candidate
from curriculum_mapper import map_candidate_topics
from question_planner import build_interview_plan


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

print("\n===== INTERVIEW PLAN =====")

for index, item in enumerate(plan, start=1):
    print(f"\nQuestion Area {index}")
    print("Day:", item["day"])
    print("Topic:", item["topic"])
    print("Difficulty:", item["difficulty"])
    print("Reason:", item["reason"])