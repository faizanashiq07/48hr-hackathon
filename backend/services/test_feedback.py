from data_loader import load_candidates
from feedback_generator import generate_feedback


data = load_candidates()

candidate = data["candidates"][0]

candidate_profile = {
    "name": candidate["member"]["name"],
    "job_role": candidate["member"]["jobRole"],
    "years_experience": candidate["member"]["yearsExperience"],
}


evaluations = [
    {
        "question": "How would you design a retrieval pipeline?",
        "answer": (
            "I would use embeddings to represent documents "
            "and retrieve the most similar chunks."
        ),
        "topic": {
            "day": 10,
            "topic": "Retrieval & Matching Engine"
        },
        "analysis": {
            "assessment": "adequate",
            "score": 6,
            "strengths": [
                "Understands the basic retrieval flow."
            ],
            "missing_concepts": [
                "Did not discuss retrieval evaluation."
            ]
        }
    },
    {
        "question": "How would you design an MCP-based system?",
        "answer": (
            "I would use MCP to standardize how models interact "
            "with external tools and resources."
        ),
        "topic": {
            "day": 23,
            "topic": "Model Context Protocol (MCP)"
        },
        "analysis": {
            "assessment": "strong",
            "score": 8,
            "strengths": [
                "Clearly explained the purpose of MCP."
            ],
            "missing_concepts": []
        }
    },
    {
        "question": "How would you approach production observability?",
        "answer": (
            "I would add logging and monitor system errors."
        ),
        "topic": {
            "day": 29,
            "topic": "Monitoring, Logging & Observability"
        },
        "analysis": {
            "assessment": "weak",
            "score": 4,
            "strengths": [
                "Recognized the importance of logging."
            ],
            "missing_concepts": [
                "Did not discuss metrics, tracing, or alerting."
            ]
        }
    }
]


feedback = generate_feedback(
    candidate_profile,
    evaluations
)


print("\n===== FINAL FEEDBACK =====\n")

print("Summary:")
print(feedback["summary"])

print("\nStrengths:")
for item in feedback["strengths"]:
    print("-", item)

print("\nGaps:")
for item in feedback["gaps"]:
    print("-", item)

print("\nRecommendations:")
for item in feedback["recommendations"]:
    print("-", item)

