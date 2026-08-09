from .candidate_analyzer import analyze_candidate
from .curriculum_mapper import map_candidate_topics
from .data_loader import load_curriculum
from .follow_up_generator import generate_follow_up
from .llm_client import generate_interviewer_response
from .question_planner import build_interview_plan
from .answer_analyzer import analyze_answer

from .session_manager import (
    create_session,
    get_session,
    record_answer,
    record_follow_up,
    advance_question,
    get_current_topic,
)


def start_interview(session_id, candidate):
    """
    Create a new interview session and generate the first question.
    """

    curriculum = load_curriculum()

    # Analyze candidate
    profile = analyze_candidate(candidate)

    # Map candidate learning history to curriculum
    mapped_topics = map_candidate_topics(
        profile,
        curriculum
    )

    # Build personalized interview plan
    interview_plan = build_interview_plan(
        profile,
        mapped_topics
    )

    if not interview_plan:
        raise ValueError(
            "Could not create an interview plan for this candidate."
        )

    # Create interview session
    session = create_session(
        session_id,
        profile,
        interview_plan
    )

    # Get first topic
    current_topic = get_current_topic(session_id)

    if current_topic is None:
        raise ValueError(
            "Interview plan does not contain a valid topic."
        )

    # No previous conversation at the beginning
    conversation_history = []

    # Generate first AI interviewer question
    question = generate_interviewer_response(
        profile,
        current_topic,
        conversation_history
    )

    session["current_question"] = question

    return {
        "reply": question,
        "done": False,
        "session_id": session_id,
    }


def process_answer(session_id, answer):
    """
    Process a candidate's answer.

    The system will either:
    1. Generate an adaptive follow-up, or
    2. Move to the next curriculum topic, or
    3. Finish the interview.
    """

    session = get_session(session_id)

    if session is None:
        raise ValueError(
            "Interview session not found."
        )

    if session["done"]:
        return {
            "reply": "The interview has already been completed.",
            "done": True,
        }

    current_topic = get_current_topic(session_id)

    if current_topic is None:
        session["done"] = True

        return {
            "reply": "The interview is complete.",
            "done": True,
        }

    # The question that the candidate is answering
    previous_question = session.get(
        "current_question",
        ""
    )

    # Preserve previous conversation
    conversation_history = session.get(
        "answers",
        []
    ).copy()

    # ---------------------------------------------------------
    # ANALYZE CANDIDATE ANSWER
    # ---------------------------------------------------------

    analysis = analyze_answer(
        session["candidate"],
        current_topic,
        previous_question,
        answer,
        conversation_history
    )

    # ---------------------------------------------------------
    # SAVE ANSWER
    # ---------------------------------------------------------

    record_answer(
        session_id,
        previous_question,
        answer
    )

    # ---------------------------------------------------------
    # SAVE EVALUATION FOR FINAL FEEDBACK
    # ---------------------------------------------------------

    session.setdefault(
        "evaluations",
        []
    )

    session["evaluations"].append(
        {
            "question": previous_question,
            "answer": answer,
            "topic": current_topic,
            "analysis": analysis,
        }
    )

    # ---------------------------------------------------------
    # ADAPTIVE FOLLOW-UP
    # ---------------------------------------------------------

    follow_up_already_used = session.get(
        "follow_up_used_for_current_topic",
        False
    )

    if (
        analysis.get("follow_up_needed", False)
        and not follow_up_already_used
    ):

        follow_up = generate_follow_up(
            session["candidate"],
            current_topic,
            previous_question,
            answer,
            analysis,
            conversation_history
        )

        record_follow_up(
            session_id,
            follow_up
        )

        session["current_question"] = follow_up

        # Allow only one follow-up per topic.
        session["follow_up_used_for_current_topic"] = True

        return {
            "reply": follow_up,
            "done": False,
        }

    # ---------------------------------------------------------
    # MOVE TO NEXT TOPIC
    # ---------------------------------------------------------

    session["follow_up_used_for_current_topic"] = False

    advance_question(session_id)

    # ---------------------------------------------------------
    # CHECK WHETHER INTERVIEW IS FINISHED
    # ---------------------------------------------------------

    if session["done"]:
        return {
            "reply": (
                "Thank you. That concludes the technical interview."
            ),
            "done": True,
        }

    # ---------------------------------------------------------
    # GENERATE NEXT QUESTION
    # ---------------------------------------------------------

    next_topic = get_current_topic(session_id)

    if next_topic is None:
        session["done"] = True

        return {
            "reply": (
                "Thank you. That concludes the technical interview."
            ),
            "done": True,
        }

    conversation_history = session.get(
        "answers",
        []
    ).copy()

    next_question = generate_interviewer_response(
        session["candidate"],
        next_topic,
        conversation_history
    )

    session["current_question"] = next_question

    return {
        "reply": next_question,
        "done": False,
    }

