from data_loader import load_candidates
from candidate_analyzer import analyze_candidate


data = load_candidates()

candidate = data["candidates"][0]

profile = analyze_candidate(candidate)

print("\n===== CANDIDATE PROFILE =====")

print("Name:", profile["name"])
print("Role:", profile["job_role"])
print("Experience:", profile["years_experience"], "years")

print("\nStrong areas:")
for topic in profile["strong_areas"]:
    print("-", topic)

print("\nWeak areas:")
for topic in profile["weak_areas"]:
    print("-", topic)

print("\nSkipped areas:")
for topic in profile["skipped_areas"]:
    print("-", topic)

print("\nHigh-effort areas:")
for topic in profile["high_effort_areas"]:
    print("-", topic["topic"], "(", topic["attempts"], "attempts )")

print("\nLearning signals:")
print(profile["learning_signals"])