"""Backend configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
PROCESSED_DIR = DATA_DIR / "processed"
APP_DATA_DIR = DATA_DIR / "app"
APP_DB_PATH = APP_DATA_DIR / "career_growth.db"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

USERS_CSV = SAMPLE_DIR / "users.csv"
EVENTS_CSV = SAMPLE_DIR / "events.csv"
EXPERIMENT_ASSIGNMENTS_CSV = SAMPLE_DIR / "experiment_assignments.csv"
INTERVENTIONS_CSV = SAMPLE_DIR / "interventions.csv"
LABELS_CSV = PROCESSED_DIR / "labels.csv"

MODEL_PATH = ARTIFACTS_DIR / "churn_model.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
MODEL_METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"
FEATURE_SCHEMA_PATH = ARTIFACTS_DIR / "feature_schema.json"
SUBGROUP_METRICS_PATH = ARTIFACTS_DIR / "subgroup_metrics.json"
USER_EXPLANATIONS_PATH = ARTIFACTS_DIR / "user_explanations.json"
NBA_EXAMPLES_PATH = ARTIFACTS_DIR / "nba_examples.json"

CUTOFF_DAY = 7
LABEL_WINDOW_START_DAY = 8
LABEL_WINDOW_END_DAY = 21
