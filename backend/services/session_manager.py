from datetime import datetime


sessions = {}


def create_session(session_id, candidate_profile, interview_plan):
    sessions[session_id] = {
        "session_id": session_id,
        "candidate": candidate_profile,
        "plan": interview_plan,
        "current_question_index": 0,
        "questions_asked": [],
        "answers": [],
        "follow_ups": [],
        "started_at": datetime.utcnow().isoformat(),
        "done": False,
    }

    return sessions[session_id]


def get_session(session_id):
    return sessions.get(session_id)


def record_answer(session_id, question, answer):
    session = get_session(session_id)

    if session is None:
        return None

    session["questions_asked"].append(question)
    session["answers"].append({
        "question": question,
        "answer": answer
    })

    return session


def record_follow_up(session_id, question):
    session = get_session(session_id)

    if session is None:
        return None

    session["follow_ups"].append(question)

    return session


def advance_question(session_id):
    session = get_session(session_id)

    if session is None:
        return None

    session["current_question_index"] += 1

    if session["current_question_index"] >= len(session["plan"]):
        session["done"] = True

    return session


def get_current_topic(session_id):
    session = get_session(session_id)

    if session is None:
        return None

    index = session["current_question_index"]

    if index >= len(session["plan"]):
        return None

    return session["plan"][index]

