import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.data_loader import load_candidates
from services.interview_controller import (
    start_interview,
    process_answer,
)
from services.feedback_generator import generate_feedback
from services.session_manager import get_session


app = FastAPI(
    title="AI Interview Agent",
    description="Adaptive technical interview agent for the AI Cohort",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Load candidate data
# ---------------------------------------------------------

candidate_data = load_candidates()


def find_candidate(member_id):
    """
    Find a candidate from the supplied candidate JSON.
    """

    for candidate in candidate_data["candidates"]:
        if candidate["member"]["id"] == member_id:
            return candidate

    return None


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class InterviewRequest(BaseModel):
    memberId: str
    sessionId: str | None = None
    message: str | None = None


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Interview Agent is running."
    }


# ---------------------------------------------------------
# Interview endpoint
# ---------------------------------------------------------

@app.post("/api/interview")
def interview(request: InterviewRequest):

    # =====================================================
    # START NEW INTERVIEW
    # =====================================================

    if request.sessionId is None:

        candidate = find_candidate(request.memberId)

        if candidate is None:
            raise HTTPException(
                status_code=404,
                detail="Candidate not found."
            )

        session_id = str(uuid.uuid4())

        try:
            result = start_interview(
                session_id,
                candidate
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=str(error)
            )

        return {
            "reply": result["reply"],
            "done": False,
            "sessionId": session_id,
        }

    # =====================================================
    # CONTINUE EXISTING INTERVIEW
    # =====================================================

    session = get_session(request.sessionId)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    if not request.message:
        raise HTTPException(
            status_code=400,
            detail="message is required when continuing an interview."
        )

    try:
        result = process_answer(
            request.sessionId,
            request.message
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    # =====================================================
    # INTERVIEW FINISHED
    # =====================================================

    if result["done"]:

        session = get_session(request.sessionId)

        feedback = generate_feedback(
            session["candidate"],
            session.get("evaluations", [])
        )

        return {
            "reply": result["reply"],
            "done": True,
            "sessionId": request.sessionId,
            "feedback": feedback,
        }

    # =====================================================
    # INTERVIEW CONTINUES
    # =====================================================

    return {
        "reply": result["reply"],
        "done": False,
        "sessionId": request.sessionId,
    }