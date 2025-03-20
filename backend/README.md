## How to run backend

Get database access in .env

1. Install dependencies

```
pip install -r requirements.txt
```

2. Run 

```
uvicorn main:app --host 0.0.0.0 --port 8082
```
---
 This app.py backend provides:

✅ AI-Powered Mock Interviews (Structured sessions with AI feedback),
✅ AI Interview Insights (Performance analysis & improvement tips)
✅ Personalized AI Interview Coach (Real-time AI-generated advice),
✅ AI-Driven Question Bank (Dynamic, resume-based questions),
✅ Adaptive Interview Difficulty (AI adjusts based on performance),
✅ Customizable AI Voice for Interviewers (AI-generated voice responses),
✅ Live AI Chat (Instant AI support for interview doubts),


---

📌 Installation Guide

1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-nexus-backend.git
cd ai-nexus-backend
```
2) Install Dependencies

```bash
pip install -r requirements.txt
```
3) Set Up OpenAI API Key

This project requires an OpenAI API Key for AI-powered features.

 Directly modify app.py
 
```python
openai.api_key = "your_openai_api_key"
```


---

🚀 Running the Backend

```bash
python app.py
```

This will start the server at:
📌 http://127.0.0.1:5000/


---

📡 API Endpoints & Usage

1️⃣ Start AI-Powered Interview

Endpoint: POST /start_interview

Payload:

```json
{
  "level": "easy"  // Options: "easy", "medium", "hard"
}
```
Response:
```json
{
  "question": "Tell me about yourself.",
  "time_limit": 900
}
```


---

2️⃣ Submit Interview Answer

Endpoint: POST /submit_answer

Payload:
```json
{
  "answer": "I am a software engineer with 3 years of experience...",
  "level": "medium"
}
```
Response:
```json
{
  "score": 78,
  "feedback": "Good answer! Try connecting your response more to your skills."
}
```


---

3️⃣ Get AI-Powered Resume-Based Questions

Endpoint: GET /resume_questions

Response:
```json
{
  "questions": [
    "Can you describe your experience with Python development?",
    "How have your past roles prepared you for this job?",
    "Tell me about a project where you used problem-solving skills."
  ]
}
```


---

4️⃣ Get AI Interview Insights

Endpoint: GET /interview_insights

Response:
```json
{
  "average_score": 82.5,
  "insights": "Your interview skills are strong. Focus on elaborating on leadership experiences."
}
```


---

5️⃣ AI Interview Coach

Endpoint: POST /interview_coach

Payload:
```json
{
  "message": "How can I improve my answers for technical interviews?"
}
```
Response:
```json
{
  "advice": "Focus on structuring your responses using the STAR method (Situation, Task, Action, Result)."
}
```


---

6️⃣ Customize AI Interview Voice

Endpoint: POST /set_voice

Payload:
```json
{
  "voice": "en"  // Change to preferred language code
}
```
Response:
```json
{
  "message": "Voice preference saved!"
}
```


---

7️⃣ Get AI Voice Interview Questions

Endpoint: POST /get_voice

Payload:
```json
{
  "question": "What are your greatest strengths?"
}
```
Response:
```json
{
  "audio_url": "/audio/user_ai_voice.mp3"
}
```
🔊 Access Audio File:
```bash
Open http://127.0.0.1:5000/audio/user_ai_voice.mp3 in your browser.
```


---

8️⃣ Live AI Chat for Interview Doubts

Endpoint: POST /chat

Payload:
```json
{
  "message": "What are common mistakes in technical interviews?"
}
```
Response:
```json
{
  "reply": "Common mistakes include lack of preparation, failing to explain thought processes, and not asking questions."
}
```


---

🔗 Deployment Guide

Using Flask in Production

For a production setup, use Gunicorn:
```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
