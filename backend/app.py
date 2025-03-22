from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import openai
import random
import os
from gtts import gTTS

app = Flask(__name__)
CORS(app)

openai.api_key = "your_openai_api_key"

# Store user data (Mock Database)
user_resumes = {}
user_interview_history = {}
user_voice_settings = {}

# ------------------------- INTERVIEW QUESTIONS BANK ------------------------- #
interview_questions = {
    "easy": [
        "Tell me about yourself.",
        "What are your strengths?",
        "Why do you want this job?"
    ],
    "medium": [
        "Describe a challenge at work and how you handled it.",
        "How do you handle feedback?",
        "Where do you see yourself in 5 years?"
    ],
    "hard": [
        "Explain a complex project you worked on.",
        "How would you handle a team conflict?",
        "What is your biggest professional failure and what did you learn?"
    ]
}

interview_timers = {"easy": 900, "medium": 1800, "hard": 2700}  

# ------------------------- AI-POWERED MOCK INTERVIEWS ------------------------- #
@app.route('/start_interview', methods=['POST'])
def start_interview():
    data = request.json
    level = data.get("level")

    if level not in interview_questions:
        return jsonify({"message": "Invalid interview level!"}), 400

    question = random.choice(interview_questions[level])
    return jsonify({"question": question, "time_limit": interview_timers[level]})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer = data.get("answer", "")
    level = data.get("level", "easy")

    resume_text = user_resumes.get("user", "")
    score = random.randint(50, 100)  

    feedback = "Try elaborating more." if len(answer) < 20 else "Good answer!"
    
    if resume_text:
        answer_words = set(answer.lower().split())
        resume_words = set(resume_text.lower().split())
        similarity_score = len(answer_words & resume_words) / max(len(answer_words), 1) * 100  
        if similarity_score > 50:
            feedback += " Your answer aligns well with your resume!"
        else:
            feedback += " Try connecting your response more to your skills."
    else:
        similarity_score = score

    if "user" not in user_interview_history:
        user_interview_history["user"] = []
    user_interview_history["user"].append({"level": level, "score": similarity_score})

    return jsonify({"score": similarity_score, "feedback": feedback})

# ------------------------- AI-BASED INTERVIEW COACH ------------------------- #
@app.route('/interview_coach', methods=['POST'])
def interview_coach():
    user_message = request.json.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI interview coach. Provide personalized advice to improve interview performance."},
            {"role": "user", "content": user_message}
        ]
    )

    coach_advice = response["choices"][0]["message"]["content"]
    return jsonify({"advice": coach_advice})

# ------------------------- RESUME-BASED AI QUESTION GENERATOR ------------------------- #
@app.route('/resume_questions', methods=['GET'])
def resume_questions():
    resume_text = user_resumes.get("user", "")

    if not resume_text:
        return jsonify({"message": "No resume uploaded!"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate three job interview questions based on this resume."},
            {"role": "user", "content": resume_text}
        ]
    )

    generated_questions = response["choices"][0]["message"]["content"]
    return jsonify({"questions": generated_questions.split("\n")})

# ------------------------- AI INTERVIEW INSIGHTS ------------------------- #
@app.route('/interview_insights', methods=['GET'])
def interview_insights():
    history = user_interview_history.get("user", [])

    if not history:
        return jsonify({"message": "No interview history found!"})

    avg_score = sum(entry["score"] for entry in history) / len(history)

    insight_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyze interview performance and provide insights."},
            {"role": "user", "content": f"My average interview score is {avg_score}%. What can I do to improve?"}
        ]
    )

    insights = insight_response["choices"][0]["message"]["content"]
    return jsonify({"average_score": avg_score, "insights": insights})

# ------------------------- AI VOICE CUSTOMIZATION ------------------------- #
@app.route('/set_voice', methods=['POST'])
def set_voice():
    data = request.json
    voice = data.get("voice", "en")  
    user_voice_settings["user"] = voice
    return jsonify({"message": "Voice preference saved!"})

@app.route('/get_voice', methods=['POST'])
def get_voice():
    question = request.json.get("question", "Welcome to your AI interview.")
    
    voice = user_voice_settings.get("user", "en")
    speech_file = f"audio/user_ai_voice.mp3"

    tts = gTTS(text=question, lang=voice)
    tts.save(speech_file)

    return jsonify({"audio_url": f"/audio/user_ai_voice.mp3"})

# ------------------------- LIVE AI CHAT ------------------------- #
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

# ------------------------- SERVING AUDIO FILES ------------------------- #
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory("audio", filename)

@app.route('/')
def home():
    return send_file('index.html')
# ------------------------- RUNNING THE APP ------------------------- #
if __name__ == '__main__':
    if not os.path.exists("audio"):
        os.makedirs("audio")
    app.run(debug=True)
