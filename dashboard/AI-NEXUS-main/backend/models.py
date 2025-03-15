# models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Text
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# 1. nexus_users
class NexusUsers(Base):
    __tablename__ = "nexus_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    notification_settings = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


# 2. nexus_resumes
class NexusResumes(Base):
    __tablename__ = "nexus_resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("nexus_users.id"), nullable=False)
    file_path = Column(String(255), nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_current = Column(Boolean, default=False)


# 3. nexus_interview_sessions
class NexusInterviewSessions(Base):
    __tablename__ = "nexus_interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("nexus_users.id"), nullable=False)
    company_type = Column(String(50), nullable=True)
    difficulty_level = Column(String(20), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)
    total_duration = Column(Integer, nullable=True)
    performance_rating = Column(Float, nullable=True)

    # New fields for dashboard metrics
    question_count = Column(Integer, nullable=True)
    average_response_time = Column(Float, nullable=True)   # e.g. seconds
    session_accuracy = Column(Float, nullable=True)        # e.g. percentage
    positive_feedback = Column(Float, nullable=True)       # e.g. percentage


# 4. nexus_interview_questions
class NexusInterviewQuestions(Base):
    __tablename__ = "nexus_interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    company_type = Column(String(50), nullable=True)
    difficulty_level = Column(String(20), nullable=True)
    category = Column(String(100), nullable=True)
    question_text = Column(Text, nullable=True)
    expected_skills = Column(ARRAY(String), nullable=True)  # array of strings
    complexity_score = Column(Integer, nullable=True)


# 5. nexus_user_responses
class NexusUserResponses(Base):
    __tablename__ = "nexus_user_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("nexus_interview_questions.id"), nullable=False)
    user_response = Column(Text, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    response_duration = Column(Integer, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)


# 6. nexus_performance_analytics
class NexusPerformanceAnalytics(Base):
    __tablename__ = "nexus_performance_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("nexus_users.id"), nullable=False)
    total_sessions = Column(Integer, nullable=True)
    average_performance = Column(Float, nullable=True)
    strongest_category = Column(String(100), nullable=True)
    weakest_category = Column(String(100), nullable=True)
    improvement_trend = Column(ARRAY(Float), nullable=True)  # array of floats


# 7. nexus_notification_log
class NexusNotificationLog(Base):
    __tablename__ = "nexus_notification_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("nexus_users.id"), nullable=False)
    notification_type = Column(String(50), nullable=True)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# 8. nexus_ai_interview_feedback
class NexusAIInterviewFeedback(Base):
    __tablename__ = "nexus_ai_interview_feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    overall_performance_summary = Column(Text, nullable=True)
    key_strengths = Column(Text, nullable=True)
    areas_for_improvement = Column(Text, nullable=True)
    recommended_resources = Column(ARRAY(String), nullable=True)  # array of strings
    generated_at = Column(DateTime, default=datetime.utcnow)


# 9. nexus_user_feedback_evaluation
class NexusUserFeedbackEvaluation(Base):
    __tablename__ = "nexus_user_feedback_evaluation"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    content_score = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)
    structure_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    example_quality_score = Column(Float, nullable=True)
    average_score = Column(Float, nullable=True)
    areas_for_improvement = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# 10. nexus_session_summary
class NexusSessionSummary(Base):
    __tablename__ = "nexus_session_summary"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    accuracy_score = Column(Float, nullable=True)
    response_time = Column(Float, nullable=True)
    feedback_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# 11. nexus_question_category_stats
class NexusQuestionCategoryStats(Base):
    __tablename__ = "nexus_question_category_stats"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    category_name = Column(String(100), nullable=True)
    question_count = Column(Integer, nullable=True)


# 12. nexus_ai_performance_metrics
class NexusAIPerformanceMetrics(Base):
    __tablename__ = "nexus_ai_performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("nexus_interview_sessions.id"), nullable=False)
    technical_accuracy_score = Column(Float, nullable=True)
    conciseness_score = Column(Float, nullable=True)
    specificity_score = Column(Float, nullable=True)
    structure_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    example_quality_score = Column(Float, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
