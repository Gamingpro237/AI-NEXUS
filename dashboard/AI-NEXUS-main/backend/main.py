from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime
from database import get_connection, release_connection
import bcrypt

app = FastAPI(title="Nexus API with Psycopg2")

# ------------------------------------------------------------------------------
# 1) nexus_users
# ------------------------------------------------------------------------------
@app.post("/register")
def register_user(email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None):
    """
    Registers a new user, hashes their password before storing in database.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Check if email already exists
            cur.execute("SELECT id FROM nexus_users WHERE email = %s", (email,))
            existing = cur.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists.")

            # Hash password before storing
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            cur.execute("""
                INSERT INTO nexus_users (email, password_hash, first_name, last_name, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, email, first_name, last_name, created_at
            """, (email, hashed_password, first_name, last_name, datetime.utcnow()))

            new_user = cur.fetchone()
            conn.commit()

        return {
            "id": new_user[0],
            "email": new_user[1],
            "first_name": new_user[2],
            "last_name": new_user[3],
            "created_at": new_user[4].isoformat() if new_user[4] else None
        }
    finally:
        release_connection(conn)

@app.post("/login")
def login_user(email: str, password: str):
    """
    Authenticates a user by verifying email and password.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, password_hash, first_name, last_name FROM nexus_users WHERE email = %s", (email,))
            user = cur.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            stored_hashed_password = user[2]
            # Verify password
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
                raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "Login successful",
            "user": {
                "id": user[0],
                "email": user[1],
                "first_name": user[3],
                "last_name": user[4]
            }
        }
    finally:
        release_connection(conn)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Deletes a user from the nexus_users table.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT id FROM nexus_users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Delete user
            cur.execute("DELETE FROM nexus_users WHERE id = %s", (user_id,))
            conn.commit()

        return {"message": f"User {user_id} has been successfully deleted"}
    finally:
        release_connection(conn)

@app.get("/nexus_users")
def get_all_users():
    """
    Lists all users from the nexus_users table.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, first_name, last_name, created_at FROM nexus_users")
            rows = cur.fetchall()
            users = []
            for row in rows:
                users.append({
                    "id": row[0],
                    "email": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "created_at": row[4].isoformat() if row[4] else None
                })
        return {"data": users}
    finally:
        release_connection(conn)

@app.post("/nexus_users")
def create_user(email: str, first_name: Optional[str] = None, last_name: Optional[str] = None):
    """
    Creates a new user in nexus_users. Minimal fields for demo.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Check if email already exists
            cur.execute("SELECT id FROM nexus_users WHERE email = %s", (email,))
            existing = cur.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists.")

            cur.execute("""
                INSERT INTO nexus_users (email, first_name, last_name, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING id, email, first_name, last_name, created_at
            """, (email, first_name, last_name, datetime.utcnow()))
            new_user = cur.fetchone()
            conn.commit()

        return {
            "id": new_user[0],
            "email": new_user[1],
            "first_name": new_user[2],
            "last_name": new_user[3],
            "created_at": new_user[4].isoformat() if new_user[4] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 2) nexus_resumes
# ------------------------------------------------------------------------------
@app.get("/nexus_resumes")
def get_all_resumes():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, user_id, file_path, upload_date, is_current FROM nexus_resumes")
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "user_id": row[1],
                    "file_path": row[2],
                    "upload_date": row[3].isoformat() if row[3] else None,
                    "is_current": row[4]
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_resumes")
def create_resume(user_id: int, file_path: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_resumes (user_id, file_path, upload_date, is_current)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, file_path, upload_date, is_current
            """, (user_id, file_path, datetime.utcnow(), False))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "user_id": row[1],
            "file_path": row[2],
            "upload_date": row[3].isoformat() if row[3] else None,
            "is_current": row[4]
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 3) nexus_interview_sessions
# ------------------------------------------------------------------------------
@app.get("/nexus_interview_sessions")
def get_all_interview_sessions():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, user_id, company_type, difficulty_level,
                       start_time, end_time, status, total_duration,
                       performance_rating, question_count,
                       average_response_time, session_accuracy,
                       positive_feedback
                FROM nexus_interview_sessions
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "user_id": row[1],
                    "company_type": row[2],
                    "difficulty_level": row[3],
                    "start_time": row[4].isoformat() if row[4] else None,
                    "end_time": row[5].isoformat() if row[5] else None,
                    "status": row[6],
                    "total_duration": row[7],
                    "performance_rating": row[8],
                    "question_count": row[9],
                    "average_response_time": row[10],
                    "session_accuracy": row[11],
                    "positive_feedback": row[12]
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_interview_sessions")
def create_interview_session(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_interview_sessions (user_id, start_time)
                VALUES (%s, %s)
                RETURNING id, user_id, start_time
            """, (user_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "user_id": row[1],
            "start_time": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 4) nexus_interview_questions
# ------------------------------------------------------------------------------
@app.get("/nexus_interview_questions")
def get_all_questions():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, company_type, difficulty_level, category,
                       question_text, expected_skills, complexity_score
                FROM nexus_interview_questions
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "company_type": row[1],
                    "difficulty_level": row[2],
                    "category": row[3],
                    "question_text": row[4],
                    "expected_skills": row[5],  # array
                    "complexity_score": row[6]
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_interview_questions")
def create_interview_question(company_type: str, difficulty_level: str, category: str, question_text: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_interview_questions (
                    company_type, difficulty_level, category, question_text
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id, company_type, difficulty_level, category, question_text
            """, (company_type, difficulty_level, category, question_text))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "company_type": row[1],
            "difficulty_level": row[2],
            "category": row[3],
            "question_text": row[4]
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 5) nexus_user_responses
# ------------------------------------------------------------------------------
@app.get("/nexus_user_responses")
def get_all_user_responses():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, question_id, user_response,
                       ai_feedback, response_duration, accuracy_score, confidence_score
                FROM nexus_user_responses
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "question_id": row[2],
                    "user_response": row[3],
                    "ai_feedback": row[4],
                    "response_duration": row[5],
                    "accuracy_score": row[6],
                    "confidence_score": row[7]
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_user_responses")
def create_user_response(session_id: int, question_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_user_responses (session_id, question_id)
                VALUES (%s, %s)
                RETURNING id, session_id, question_id
            """, (session_id, question_id))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "question_id": row[2]
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 6) nexus_performance_analytics
# ------------------------------------------------------------------------------
@app.get("/nexus_performance_analytics")
def get_all_performance_analytics():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, user_id, total_sessions, average_performance,
                       strongest_category, weakest_category, improvement_trend
                FROM nexus_performance_analytics
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "user_id": row[1],
                    "total_sessions": row[2],
                    "average_performance": row[3],
                    "strongest_category": row[4],
                    "weakest_category": row[5],
                    "improvement_trend": row[6]  # array
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_performance_analytics")
def create_performance_analytics(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_performance_analytics (user_id, total_sessions, average_performance)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, total_sessions, average_performance
            """, (user_id, 0, 0.0))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "user_id": row[1],
            "total_sessions": row[2],
            "average_performance": row[3]
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 7) nexus_notification_log
# ------------------------------------------------------------------------------
@app.get("/nexus_notification_log")
def get_all_notification_logs():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, user_id, notification_type, message, is_read, created_at
                FROM nexus_notification_log
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "user_id": row[1],
                    "notification_type": row[2],
                    "message": row[3],
                    "is_read": row[4],
                    "created_at": row[5].isoformat() if row[5] else None
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_notification_log")
def create_notification_log(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_notification_log (user_id, created_at)
                VALUES (%s, %s)
                RETURNING id, user_id, created_at
            """, (user_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "user_id": row[1],
            "created_at": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 8) nexus_ai_interview_feedback
# ------------------------------------------------------------------------------
@app.get("/nexus_ai_interview_feedback")
def get_all_ai_feedback():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, overall_performance_summary, key_strengths,
                       areas_for_improvement, recommended_resources, generated_at
                FROM nexus_ai_interview_feedback
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "overall_performance_summary": row[2],
                    "key_strengths": row[3],
                    "areas_for_improvement": row[4],
                    "recommended_resources": row[5],  # array
                    "generated_at": row[6].isoformat() if row[6] else None
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_ai_interview_feedback")
def create_ai_feedback(session_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_ai_interview_feedback (session_id, generated_at)
                VALUES (%s, %s)
                RETURNING id, session_id, generated_at
            """, (session_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "generated_at": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 9) nexus_user_feedback_evaluation
# ------------------------------------------------------------------------------
@app.get("/nexus_user_feedback_evaluation")
def get_all_feedback_evals():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, content_score, clarity_score,
                       structure_score, relevance_score, example_quality_score,
                       average_score, areas_for_improvement, created_at
                FROM nexus_user_feedback_evaluation
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "content_score": row[2],
                    "clarity_score": row[3],
                    "structure_score": row[4],
                    "relevance_score": row[5],
                    "example_quality_score": row[6],
                    "average_score": row[7],
                    "areas_for_improvement": row[8],
                    "created_at": row[9].isoformat() if row[9] else None
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_user_feedback_evaluation")
def create_feedback_eval(session_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_user_feedback_evaluation (session_id, created_at)
                VALUES (%s, %s)
                RETURNING id, session_id, created_at
            """, (session_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "created_at": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 10) nexus_session_summary
# ------------------------------------------------------------------------------
@app.get("/nexus_session_summary")
def get_all_session_summaries():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, accuracy_score, response_time,
                       feedback_score, created_at
                FROM nexus_session_summary
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "accuracy_score": row[2],
                    "response_time": row[3],
                    "feedback_score": row[4],
                    "created_at": row[5].isoformat() if row[5] else None
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_session_summary")
def create_session_summary(session_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_session_summary (session_id, created_at)
                VALUES (%s, %s)
                RETURNING id, session_id, created_at
            """, (session_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "created_at": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 11) nexus_question_category_stats
# ------------------------------------------------------------------------------
@app.get("/nexus_question_category_stats")
def get_all_qcategory_stats():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, category_name, question_count
                FROM nexus_question_category_stats
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "category_name": row[2],
                    "question_count": row[3]
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_question_category_stats")
def create_qcategory_stats(session_id: int, category_name: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_question_category_stats (session_id, category_name, question_count)
                VALUES (%s, %s, %s)
                RETURNING id, session_id, category_name, question_count
            """, (session_id, category_name, 0))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "category_name": row[2],
            "question_count": row[3]
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# 12) nexus_ai_performance_metrics
# ------------------------------------------------------------------------------
@app.get("/nexus_ai_performance_metrics")
def get_all_ai_perf_metrics():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, session_id, technical_accuracy_score, conciseness_score,
                       specificity_score, structure_score, relevance_score,
                       example_quality_score, generated_at
                FROM nexus_ai_performance_metrics
            """)
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "session_id": row[1],
                    "technical_accuracy_score": row[2],
                    "conciseness_score": row[3],
                    "specificity_score": row[4],
                    "structure_score": row[5],
                    "relevance_score": row[6],
                    "example_quality_score": row[7],
                    "generated_at": row[8].isoformat() if row[8] else None
                })
        return {"data": data}
    finally:
        release_connection(conn)

@app.post("/nexus_ai_performance_metrics")
def create_ai_perf_metrics(session_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_ai_performance_metrics (session_id, generated_at)
                VALUES (%s, %s)
                RETURNING id, session_id, generated_at
            """, (session_id, datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
        return {
            "id": row[0],
            "session_id": row[1],
            "generated_at": row[2].isoformat() if row[2] else None
        }
    finally:
        release_connection(conn)

# ------------------------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------------------------
@app.get("/")
def read_root():
    """
    Basic health check or welcome message.
    """
    return {"message": "Welcome to the Nexus API (psycopg2)!"}
