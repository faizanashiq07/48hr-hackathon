from data_loader import load_candidates, load_curriculum
from candidate_analyzer import analyze_candidate
from curriculum_mapper import map_candidate_topics


candidates = load_candidates()
curriculum = load_curriculum()

candidate = candidates["candidates"][0]

profile = analyze_candidate(candidate)

topics = map_candidate_topics(profile, curriculum)

print("\n===== CURRICULUM MAPPING =====")

for topic in topics:
    print(f"\nDay {topic['day']}: {topic['title']}")
    print("Type:", topic["type"])
    print("Tools:", ", ".join(topic["tools"]))

    print("Objectives:")
    for objective in topic["objectives"]:
        print(" -", objective)