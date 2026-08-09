def build_interview_plan(candidate_profile, mapped_topics, max_questions=10):
    candidates = []

    strong_topics = set(candidate_profile["strong_areas"])
    weak_topics = set(candidate_profile["weak_areas"])
    skipped_topics = set(candidate_profile["skipped_areas"])

    high_effort_lookup = {
        item["topic"]: item["attempts"]
        for item in candidate_profile["high_effort_areas"]
    }

    for topic in mapped_topics:
        title = topic["title"]

        if title in strong_topics:
            attempts = high_effort_lookup.get(title, 1)

            if attempts >= 3:
                difficulty = "advanced"
                priority = 3
                reason = (
                    "Completed successfully but required multiple attempts, "
                    "so deeper understanding should be probed."
                )
            else:
                difficulty = "advanced"
                priority = 2
                reason = (
                    "Completed successfully, making it suitable for "
                    "deeper technical questioning."
                )

            candidates.append({
                "day": topic["day"],
                "topic": title,
                "difficulty": difficulty,
                "priority": priority,
                "reason": reason,
                "objectives": topic["objectives"]
            })

        elif title in weak_topics:
            candidates.append({
                "day": topic["day"],
                "topic": title,
                "difficulty": "intermediate",
                "priority": 3,
                "reason": (
                    "Candidate has an unsuccessful learning signal "
                    "for this topic and should be probed."
                ),
                "objectives": topic["objectives"]
            })

        elif title in skipped_topics:
            candidates.append({
                "day": topic["day"],
                "topic": title,
                "difficulty": "intermediate",
                "priority": 2,
                "reason": (
                    "Candidate skipped this topic, so the interview "
                    "should determine their actual understanding."
                ),
                "objectives": topic["objectives"]
            })

    # Higher-priority topics first.
    candidates.sort(
        key=lambda item: (-item["priority"], item["day"])
    )

    # Select topics while trying to maximize curriculum-day diversity.
    selected = []
    selected_days = set()

    # First pass: one topic from each different curriculum day.
    for item in candidates:
        if item["day"] not in selected_days:
            selected.append(item)
            selected_days.add(item["day"])

        if len(selected) >= max_questions:
            break

    # Second pass: fill remaining slots.
    if len(selected) < max_questions:
        for item in candidates:
            if item not in selected:
                selected.append(item)

            if len(selected) >= max_questions:
                break

    return selected

