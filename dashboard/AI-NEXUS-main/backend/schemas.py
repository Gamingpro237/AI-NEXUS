from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ----------------------------------------------------------------------
# 1. nexus_users
# ----------------------------------------------------------------------
class NexusUserBase(BaseModel):
    email: str
    password_hash: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    contact_email: Optional[str] = None
    notification_settings: Optional[bool] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

class NexusUserCreate(BaseModel):
    email: str
    password_hash: str

class NexusUser(NexusUserBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 2. nexus_resumes
# ----------------------------------------------------------------------
class NexusResumeBase(BaseModel):
    user_id: int
    file_path: Optional[str] = None
    upload_date: Optional[datetime] = None
    is_current: Optional[bool] = None

class NexusResumeCreate(BaseModel):
    user_id: int
    file_path: str

class NexusResume(NexusResumeBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 3. nexus_interview_sessions
# ----------------------------------------------------------------------
class NexusInterviewSessionBase(BaseModel):
    user_id: int
    company_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    total_duration: Optional[int] = None
    performance_rating: Optional[float] = None
    question_count: Optional[int] = None
    average_response_time: Optional[float] = None
    session_accuracy: Optional[float] = None
    positive_feedback: Optional[float] = None

class NexusInterviewSessionCreate(BaseModel):
    user_id: int

class NexusInterviewSession(NexusInterviewSessionBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 4. nexus_interview_questions
# ----------------------------------------------------------------------
from typing import List as TypingList  # to avoid confusion with pydantic List

class NexusInterviewQuestionBase(BaseModel):
    company_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    category: Optional[str] = None
    question_text: Optional[str] = None
    expected_skills: Optional[TypingList[str]] = None
    complexity_score: Optional[int] = None

class NexusInterviewQuestionCreate(BaseModel):
    company_type: str
    difficulty_level: str
    category: str
    question_text: str

class NexusInterviewQuestion(NexusInterviewQuestionBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 5. nexus_user_responses
# ----------------------------------------------------------------------
class NexusUserResponseBase(BaseModel):
    session_id: int
    question_id: int
    user_response: Optional[str] = None
    ai_feedback: Optional[str] = None
    response_duration: Optional[int] = None
    accuracy_score: Optional[float] = None
    confidence_score: Optional[float] = None

class NexusUserResponseCreate(BaseModel):
    session_id: int
    question_id: int

class NexusUserResponse(NexusUserResponseBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 6. nexus_performance_analytics
# ----------------------------------------------------------------------
class NexusPerformanceAnalyticsBase(BaseModel):
    user_id: int
    total_sessions: Optional[int] = None
    average_performance: Optional[float] = None
    strongest_category: Optional[str] = None
    weakest_category: Optional[str] = None
    improvement_trend: Optional[List[float]] = None

class NexusPerformanceAnalyticsCreate(BaseModel):
    user_id: int

class NexusPerformanceAnalytics(NexusPerformanceAnalyticsBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 7. nexus_notification_log
# ----------------------------------------------------------------------
class NexusNotificationLogBase(BaseModel):
    user_id: int
    notification_type: Optional[str] = None
    message: Optional[str] = None
    is_read: Optional[bool] = None
    created_at: Optional[datetime] = None

class NexusNotificationLogCreate(BaseModel):
    user_id: int

class NexusNotificationLog(NexusNotificationLogBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 8. nexus_ai_interview_feedback
# ----------------------------------------------------------------------
class NexusAIInterviewFeedbackBase(BaseModel):
    session_id: int
    overall_performance_summary: Optional[str] = None
    key_strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    recommended_resources: Optional[List[str]] = None
    generated_at: Optional[datetime] = None

class NexusAIInterviewFeedbackCreate(BaseModel):
    session_id: int

class NexusAIInterviewFeedback(NexusAIInterviewFeedbackBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 9. nexus_user_feedback_evaluation
# ----------------------------------------------------------------------
class NexusUserFeedbackEvaluationBase(BaseModel):
    session_id: int
    content_score: Optional[float] = None
    clarity_score: Optional[float] = None
    structure_score: Optional[float] = None
    relevance_score: Optional[float] = None
    example_quality_score: Optional[float] = None
    average_score: Optional[float] = None
    areas_for_improvement: Optional[str] = None
    created_at: Optional[datetime] = None

class NexusUserFeedbackEvaluationCreate(BaseModel):
    session_id: int

class NexusUserFeedbackEvaluation(NexusUserFeedbackEvaluationBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 10. nexus_session_summary
# ----------------------------------------------------------------------
class NexusSessionSummaryBase(BaseModel):
    session_id: int
    accuracy_score: Optional[float] = None
    response_time: Optional[float] = None
    feedback_score: Optional[float] = None
    created_at: Optional[datetime] = None

class NexusSessionSummaryCreate(BaseModel):
    session_id: int

class NexusSessionSummary(NexusSessionSummaryBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 11. nexus_question_category_stats
# ----------------------------------------------------------------------
class NexusQuestionCategoryStatsBase(BaseModel):
    session_id: int
    category_name: Optional[str] = None
    question_count: Optional[int] = None

class NexusQuestionCategoryStatsCreate(BaseModel):
    session_id: int
    category_name: str

class NexusQuestionCategoryStats(NexusQuestionCategoryStatsBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------
# 12. nexus_ai_performance_metrics
# ----------------------------------------------------------------------
class NexusAIPerformanceMetricsBase(BaseModel):
    session_id: int
    technical_accuracy_score: Optional[float] = None
    conciseness_score: Optional[float] = None
    specificity_score: Optional[float] = None
    structure_score: Optional[float] = None
    relevance_score: Optional[float] = None
    example_quality_score: Optional[float] = None
    generated_at: Optional[datetime] = None

class NexusAIPerformanceMetricsCreate(BaseModel):
    session_id: int

class NexusAIPerformanceMetrics(NexusAIPerformanceMetricsBase):
    id: int

    class Config:
        orm_mode = True
