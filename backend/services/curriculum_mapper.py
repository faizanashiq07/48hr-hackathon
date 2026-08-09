def build_curriculum_index(curriculum):
    index = {}

    for day in curriculum.get("days", []):
        index[day["title"]] = {
            "day": day["day"],
            "title": day["title"],
            "type": day.get("type"),
            "tools": day.get("tools", []),
            "objectives": day.get("objectives", [])
        }

    return index


def map_candidate_topics(candidate_profile, curriculum):
    curriculum_index = build_curriculum_index(curriculum)

    mapped = []

    all_topics = (
        candidate_profile["strong_areas"]
        + candidate_profile["weak_areas"]
        + candidate_profile["skipped_areas"]
    )

    seen = set()

    for topic in all_topics:
        if topic in seen:
            continue

        seen.add(topic)

        if topic in curriculum_index:
            mapped.append(curriculum_index[topic])

    return mapped

