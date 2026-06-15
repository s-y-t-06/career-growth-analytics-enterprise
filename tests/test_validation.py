"""Tests for the data validation module."""

from career_growth.validation.validator import DataValidator


def test_validator_passes_on_generated_data(synthetic_data):
    validator = DataValidator("data_test_shared")
    validator.users = synthetic_data["users"]
    validator.events = synthetic_data["events"]
    validator.experiment_assignments = synthetic_data["experiment_assignments"]
    validator.interventions = synthetic_data["interventions"]
    validator.labels = synthetic_data["labels"]
    report = validator.validate()
    assert report.passed, f"Validation failed: {report.errors}"


def test_validator_detects_orphan_event():
    from career_growth.data_generation.generator import generate_all_data

    data = generate_all_data(count=100, seed=42, output_dir="data_test_orphan")
    validator = DataValidator("data_test_orphan").load()
    validator.events.loc[0, "user_id"] = "nonexistent-user"
    report = validator.validate()
    assert not report.passed
    assert any("unknown user_id" in err for err in report.errors)


def test_validator_detects_invalid_event_source():
    from career_growth.data_generation.generator import generate_all_data

    data = generate_all_data(count=100, seed=42, output_dir="data_test_source")
    validator = DataValidator("data_test_source").load()
    validator.events.loc[0, "event_source"] = "bot"
    report = validator.validate()
    assert not report.passed
    assert any("event_source" in err for err in report.errors)


def test_validator_detects_duplicate_event_id():
    from career_growth.data_generation.generator import generate_all_data

    data = generate_all_data(count=100, seed=42, output_dir="data_test_dup")
    validator = DataValidator("data_test_dup").load()
    validator.events.loc[1, "event_id"] = validator.events.loc[0, "event_id"]
    report = validator.validate()
    assert not report.passed
    assert any("duplicate event_id" in err for err in report.errors)
