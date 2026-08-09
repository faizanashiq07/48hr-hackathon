from data_loader import load_candidates, load_curriculum


candidates = load_candidates()
curriculum = load_curriculum()

print("Candidates loaded:", len(candidates["candidates"]))
print("Curriculum modules:", len(curriculum["modules"]))
print("Curriculum days:", len(curriculum["days"]))

print("\nFirst candidate:")
print(candidates["candidates"][0]["member"]["name"])

print("\nFirst curriculum day:")
print(curriculum["days"][0]["title"])

