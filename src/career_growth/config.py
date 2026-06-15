"""MVP 合成数据管道的项目级配置。"""

from datetime import datetime, timedelta, timezone
from typing import Final

RANDOM_SEED: Final[int] = 42

# 数据生成的全局观察窗口。
# 用户在 90 天内生成，截止日期为数据冻结前 21 天，
# 以确保每个用户都有完整的流失标签窗口。
END_DATE: Final[datetime] = datetime(2026, 6, 1, 23, 59, 59, tzinfo=timezone.utc)
STUDY_START_DATE: Final[datetime] = END_DATE - timedelta(days=90)

# 要生成的合成用户数量。
DEFAULT_USER_COUNT: Final[int] = 5_000

# 注册后用于定义流失标签的天数窗口。
PREDICTION_CUTOFF_DAY: Final[int] = 7
LABEL_WINDOW_START_DAY: Final[int] = 8
LABEL_WINDOW_END_DAY: Final[int] = 21

# 获客渠道及其预期占比。
ACQUISITION_CHANNELS: Final[list[str]] = [
    "organic_search",
    "social_ads",
    "campus_event",
    "referral",
    "content_marketing",
]
ACQUISITION_CHANNEL_WEIGHTS: Final[list[float]] = [0.35, 0.25, 0.20, 0.10, 0.10]

# 设备类型。
DEVICE_TYPES: Final[list[str]] = ["desktop", "mobile", "tablet"]
DEVICE_TYPE_WEIGHTS: Final[list[float]] = [0.45, 0.40, 0.15]

# 国家、语言和时区。
COUNTRY_CONFIG: Final[dict[str, dict[str, str]]] = {
    "US": {"language": "en", "timezone": "America/New_York"},
    "CN": {"language": "zh", "timezone": "Asia/Shanghai"},
    "IN": {"language": "en", "timezone": "Asia/Kolkata"},
    "GB": {"language": "en", "timezone": "Europe/London"},
    "DE": {"language": "de", "timezone": "Europe/Berlin"},
    "CA": {"language": "en", "timezone": "America/Toronto"},
    "BR": {"language": "pt", "timezone": "America/Sao_Paulo"},
    "FR": {"language": "fr", "timezone": "Europe/Paris"},
    "JP": {"language": "ja", "timezone": "Asia/Tokyo"},
    "AU": {"language": "en", "timezone": "Australia/Sydney"},
}
COUNTRY_WEIGHTS: Final[list[float]] = [0.35, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02, 0.02, 0.02, 0.01]

# 职业阶段。
CAREER_STAGES: Final[list[str]] = ["student", "new_graduate", "early_career"]
CAREER_STAGE_WEIGHTS: Final[list[float]] = [0.45, 0.30, 0.25]

# 用户意向等级。
USER_INTENT_LEVELS: Final[list[str]] = ["low", "medium", "high"]
USER_INTENT_WEIGHTS: Final[list[float]] = [0.30, 0.45, 0.25]

# 核心事件名称。
CORE_EVENTS: Final[list[str]] = [
    "signup",
    "onboarding_start",
    "onboarding_complete",
    "profile_complete",
    "resume_upload",
    "job_recommendation_view",
    "job_save",
    "growth_task_complete",
    "career_report_generate",
]

# 事件流中允许的附加事件。
EXTRA_EVENTS: Final[list[str]] = [
    "session_start",
    "session_end",
    "job_detail_view",
    "ai_assistant_interaction",
    "return_visit",
    "email_sent",
    "push_sent",
    "in_app_message_sent",
]

ALL_EVENT_NAMES: Final[list[str]] = CORE_EVENTS + EXTRA_EVENTS

# 事件来源取值。
EVENT_SOURCES: Final[list[str]] = ["user_action", "system", "campaign"]

# 新手引导实验定义。
ONBOARDING_EXPERIMENT_ID: Final[str] = "exp_onboarding_v1"
ONBOARDING_EXPERIMENT_NAME: Final[str] = "Onboarding Flow Optimization"
ONBOARDING_VARIANTS: Final[list[dict[str, str | float]]] = [
    {"variant_id": "control", "name": "standard five-step onboarding", "allocation": 0.40, "effect": 0.0},
    {"variant_id": "personalized", "name": "adaptive onboarding", "allocation": 0.30, "effect": 0.30},
    {"variant_id": "simplified", "name": "two-step onboarding", "allocation": 0.30, "effect": 0.15},
]

# 分析中使用的漏斗步骤。
FUNNEL_STEPS: Final[list[str]] = [
    "signup",
    "onboarding_complete",
    "profile_complete",
    "resume_upload",
    "job_recommendation_view",
    "job_save",
    "career_report_generate",
]

# 数据输出路径。
SAMPLE_DATA_DIR: Final[str] = "data/sample"
PROCESSED_DATA_DIR: Final[str] = "data/processed"
