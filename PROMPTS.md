# \# AI Usage Log

##### 

# \## Project

# InterviewAI — Adaptive Technical Interview Platform

##### 

## \## AI Tool Used

## ChatGPT

##### 

#### \## Purpose of AI Assistance

##### AI assistance was used throughout development for brainstorming, debugging,

##### implementation guidance, prompt engineering, API integration, deployment,

##### and troubleshooting.

##### 

#### \## Development Prompts / Usage

#### 

#### \### 1. Project and Hackathon Guidance

##### Used ChatGPT to:

##### \- Understand the hackathon requirements.

##### \- Plan the technical implementation.

##### \- Break the project into frontend, backend, AI evaluation, and deployment tasks.

##### \- Decide how to structure the application for a working live demonstration.

##### 

#### \### 2. Interview Prompt Engineering

##### Prompts were designed for an AI technical interviewer to:

##### \- Evaluate technical correctness, depth, reasoning, relevance, and practical understanding.

##### \- Adapt follow-up questions based on the candidate's previous answers.

##### \- Identify strengths and missing concepts.

##### \- Decide when a targeted follow-up question is useful.

##### \- Maintain a consistent interview evaluation structure.

##### 

##### Example evaluator instruction:

##### 

##### > You are an expert technical interview evaluator. Evaluate a candidate's

##### > answer based on technical correctness, depth of understanding, reasoning,

##### > relevance to the question, and ability to apply concepts.

##### 

##### The evaluator was instructed to return structured JSON containing:

##### \- assessment

##### \- score

##### \- strengths

##### \- missing concepts

##### \- follow-up requirement

##### \- follow-up reason

##### \- suggested follow-up focus

##### 

#### \### 3. Prompt Engineering Evaluation

##### ChatGPT was used to reason about:

##### \- Zero-shot prompting

##### \- Few-shot prompting

##### \- Chain-of-thought prompting

##### \- Friendly and empathetic chatbot tone

##### \- Brand guideline compliance

##### \- Evaluation metrics for prompt effectiveness

##### 

#### \### 4. Backend Development and Debugging

##### ChatGPT was used to troubleshoot:

##### \- FastAPI API routes

##### \- Python environment setup

##### \- Missing Python dependencies

##### \- Groq API integration

##### \- API request failures

##### \- HTTP 404 and 500 errors

##### \- Groq token/rate-limit errors

##### \- Environment variable configuration

##### 

#### \### 5. Frontend Development

##### ChatGPT was used to:

##### \- Build and modify the React/Vite interview interface.

##### \- Fix JSX parsing errors.

##### \- Structure the interview question and answer flow.

##### \- Create the completion/results experience.

##### \- Debug frontend-to-backend communication.

##### 

#### \### 6. Deployment

##### ChatGPT was used to troubleshoot deployment using:

##### \- Git and GitHub

##### \- Vercel

##### \- FastAPI serverless deployment

##### \- Vercel Python entry points

##### \- Environment variables

##### \- Production API routing

##### 

#### \### 7. Testing

##### The application was tested locally and in production.

##### 

##### Testing included:

##### \- Starting an interview.

##### \- Submitting candidate answers.

##### \- Generating subsequent questions.

##### \- Evaluating answers using the AI backend.

##### \- Completing the interview.

##### \- Testing the deployed application in an incognito browser session.

##### 

##### \## Important AI-Assisted Implementation

##### The final application uses an AI-backed interview evaluation pipeline in which

##### candidate answers are sent to the backend, evaluated against the current

##### curriculum topic and question, and used to determine whether a targeted

##### follow-up is required.

##### 

##### \## Human Validation

##### All AI-generated implementation suggestions were reviewed and tested by the

##### developer. Code was modified, executed locally, debugged, committed to Git,

##### deployed, and verified through the live application.

##### 

##### \## Final Verification

##### The deployed InterviewAI application was successfully tested in an incognito

##### browser. The interview completed successfully and AI evaluation was confirmed.

