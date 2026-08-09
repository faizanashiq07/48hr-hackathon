import { useState } from "react";
import "./App.css";

const API_URL = "https://48hr-hackathon-6cxq.vercel.app";
const MAX_QUESTIONS = 15;

function App() {
  const [memberId, setMemberId] = useState("CAND-001");
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [messages, setMessages] = useState([]);
  const [started, setStarted] = useState(false);
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(false);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [error, setError] = useState("");

  async function startInterview() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          memberId: memberId,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || "Failed to start interview");
      }

      setSessionId(data.sessionId);
      setQuestion(data.reply || "");
      setQuestionNumber(1);

      setMessages([
        {
          role: "ai",
          text: data.reply || "",
        },
      ]);

      setStarted(true);
      setFinished(false);
    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to the interview server. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (!answer.trim() || loading) {
      return;
    }

    const currentAnswer = answer.trim();

    setMessages((oldMessages) => [
      ...oldMessages,
      {
        role: "candidate",
        text: currentAnswer,
      },
    ]);

    setAnswer("");

    /*
     * CRITICAL:
     * If this is Q15, finish immediately.
     * We DO NOT call the backend.
     */
    if (questionNumber >= MAX_QUESTIONS) {
      setQuestion("");
      setFinished(true);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          memberId: memberId,
          sessionId: sessionId,
          message: currentAnswer,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail || "Failed to process answer"
        );
      }

      if (data.done) {
        setQuestion("");
        setFinished(true);
        return;
      }

      if (data.reply) {
        setMessages((oldMessages) => [
          ...oldMessages,
          {
            role: "ai",
            text: data.reply,
          },
        ]);

        setQuestion(data.reply);
      }

      setQuestionNumber((number) => number + 1);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to process your answer. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !loading &&
      started &&
      !finished
    ) {
      event.preventDefault();
      submitAnswer();
    }
  }

  /* ================= LANDING ================= */

  if (!started) {
    return (
      <div className="app">
        <header className="topbar">
          <div className="brand">
            <div className="brand-icon">AI</div>

            <div>
              <h2>InterviewAI</h2>
              <span>Adaptive Technical Interviewer</span>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            AI Ready
          </div>
        </header>

        <main className="landing">
          <div className="hero-badge">
            ✦ AI-POWERED TECHNICAL INTERVIEW
          </div>

          <h1>
            Your skills.
            <br />
            <span>Tested intelligently.</span>
          </h1>

          <p className="hero-text">
            An adaptive technical interview that evaluates your
            knowledge, adjusts question difficulty, and provides
            personalized feedback.
          </p>

          <div className="start-card">
            <div className="card-icon">◆</div>

            <h2>Ready for your interview?</h2>

            <p>
              Answer naturally. The AI interviewer will adapt
              based on your responses.
            </p>

            <label htmlFor="candidateId">
              Candidate ID
            </label>

            <input
              id="candidateId"
              value={memberId}
              onChange={(event) =>
                setMemberId(event.target.value)
              }
              placeholder="Enter candidate ID"
            />

            <button
              className="primary-button"
              onClick={startInterview}
              disabled={
                loading || !memberId.trim()
              }
            >
              {loading ? "Starting..." : "Start Interview →"}
            </button>

            {error && (
              <div className="error">
                {error}
              </div>
            )}
          </div>

          <div className="features">
            <div>
              <strong>01</strong>
              <span>Adaptive questions</span>
            </div>

            <div>
              <strong>02</strong>
              <span>Real-time evaluation</span>
            </div>

            <div>
              <strong>03</strong>
              <span>Personalized feedback</span>
            </div>
          </div>
        </main>
      </div>
    );
  }

  /* ================= FINISHED ================= */

  if (finished) {
    return (
      <div className="app">
        <header className="topbar">
          <div className="brand">
            <div className="brand-icon">AI</div>

            <div>
              <h2>InterviewAI</h2>
              <span>Interview Complete</span>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            Completed
          </div>
        </header>

        <main className="finished">
          <div className="success-icon">✓</div>

          <div className="hero-badge">
            INTERVIEW COMPLETE
          </div>

          <h1>
            Great work, <span>{memberId}</span>.
          </h1>

          <p>
            You completed your adaptive technical interview.
            Your responses were evaluated across multiple
            technical areas.
          </p>

          <div className="feedback-card">
            <div className="feedback-header">
              <span>AI INTERVIEW SUMMARY</span>
              <span className="check">✓</span>
            </div>

            <div className="feedback-content">
              <p>
                Interview completed successfully.
                Your answers were evaluated by the AI
                interviewer based on technical correctness,
                reasoning, depth, and practical understanding.
              </p>

              <div className="features">
                <div>
                  <strong>15</strong>
                  <span>Questions</span>
                </div>

                <div>
                  <strong>AI</strong>
                  <span>Adaptive evaluation</span>
                </div>

                <div>
                  <strong>✓</strong>
                  <span>Completed</span>
                </div>
              </div>
            </div>
          </div>

          <button
            className="primary-button"
            onClick={() => window.location.reload()}
          >
            Start New Interview →
          </button>
        </main>
      </div>
    );
  }

  /* ================= INTERVIEW ================= */

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h2>InterviewAI</h2>
            <span>Adaptive Technical Interview</span>
          </div>
        </div>

        <div className="question-counter">
          QUESTION{" "}
          <strong>
            {questionNumber}/{MAX_QUESTIONS}
          </strong>
        </div>
      </header>

      <main className="interview-container">
        <div className="progress-wrapper">
          <div className="progress-label">
            <span>Interview Progress</span>

            <span>
              Question {questionNumber} of {MAX_QUESTIONS}
            </span>
          </div>

          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${
                  (questionNumber / MAX_QUESTIONS) * 100
                }%`,
              }}
            ></div>
          </div>
        </div>

        <div className="interview-grid">
          <section className="conversation">
            <div className="ai-message">
              <div className="avatar">AI</div>

              <div className="message-content">
                <div className="message-name">
                  AI INTERVIEWER
                </div>

                <div className="question-box">
                  {question}
                </div>
              </div>
            </div>

            {messages.map((message, index) => {
              if (message.role !== "candidate") {
                return null;
              }

              return (
                <div
                  className="candidate-message"
                  key={index}
                >
                  <div className="message-name">
                    YOU
                  </div>

                  <div className="candidate-box">
                    {message.text}
                  </div>
                </div>
              );
            })}
          </section>

          <aside className="answer-panel">
            <div className="panel-header">
              <span>Your answer</span>

              <span className="hint">
                Enter to submit
              </span>
            </div>

            <textarea
              value={answer}
              onChange={(event) =>
                setAnswer(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Type your answer here..."
              disabled={loading}
            ></textarea>

            <div className="answer-footer">
              <span>
                {answer.length} characters
              </span>

              <button
                className="submit-button"
                onClick={submitAnswer}
                disabled={
                  loading || !answer.trim()
                }
              >
                {loading
                  ? "Evaluating..."
                  : "Submit Answer →"}
              </button>
            </div>

            {error && (
              <div className="error">
                {error}
              </div>
            )}
          </aside>
        </div>

        <div className="interview-tip">
          <span>✦</span>{" "}
          <strong>Tip:</strong>{" "}
          Explain your reasoning, not just the final answer.
        </div>
      </main>
    </div>
  );
}

export default App;