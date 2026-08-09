def analyze_candidate(candidate):
    member = candidate["member"]
    missions = candidate.get("missions", [])
    signals = candidate.get("signals", {})

    strong_areas = []
    weak_areas = []
    skipped_areas = []
    high_effort_areas = []

    for mission in missions:
        title = mission["title"]
        passed = mission.get("passed", False)
        skipped = mission.get("skipped", False)
        attempts = mission.get("attempts", 0)

        if skipped:
            skipped_areas.append(title)
            continue

        if passed:
            strong_areas.append(title)

            if attempts >= 3:
                high_effort_areas.append({
                    "topic": title,
                    "attempts": attempts
                })

        else:
            weak_areas.append(title)

    return {
        "id": member["id"],
        "name": member["name"],
        "job_role": member["jobRole"],
        "years_experience": member["yearsExperience"],
        "education": member["education"],
        "status": member["status"],
        "strong_areas": strong_areas,
        "weak_areas": weak_areas,
        "skipped_areas": skipped_areas,
        "high_effort_areas": high_effort_areas,
        "learning_signals": signals
    }

