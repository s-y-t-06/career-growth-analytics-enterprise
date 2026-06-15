"""Train and evaluate a churn prediction model for Career Growth Analytics."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import joblib
import numpy as np
import pandas as pd

from career_growth import config
from career_growth.data_generation.generator import generate_all_data
from career_growth.features.model_features import prepare_model_matrix
from career_growth.modeling.evaluate import compute_calibration_data
from career_growth.modeling.explain import (
    compute_permutation_importance,
    extract_logistic_coefficients,
)
from career_growth.modeling.split import split_users_and_labels
from career_growth.modeling.train import save_model, train_and_select_model


DEFAULT_OUTPUT_DIR: str = "artifacts"
PLOT_DIR: str = "plots"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Train churn prediction models and save evaluation artifacts."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=config.DEFAULT_USER_COUNT,
        help="Number of synthetic users to generate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=config.RANDOM_SEED,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory containing generated data or used for output.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for model artifacts and metrics.",
    )
    parser.add_argument(
        "--threshold-criterion",
        type=str,
        default="f1",
        choices=["f1", "precision", "recall", "f2", "youden"],
        help="Criterion used to select the operating threshold on validation data.",
    )
    parser.add_argument(
        "--use-existing-data",
        action="store_true",
        help="Load existing CSV files from data-dir instead of regenerating them.",
    )
    return parser.parse_args()


def ensure_data(args: argparse.Namespace) -> dict[str, pd.DataFrame]:
    """Generate or load synthetic data."""
    data_dir = Path(args.data_dir)
    sample_dir = data_dir / "sample"
    processed_dir = data_dir / "processed"

    if args.use_existing_data and (sample_dir / "users.csv").exists():
        print(f"Loading existing data from {data_dir}")
        return {
            "users": pd.read_csv(sample_dir / "users.csv"),
            "events": pd.read_csv(sample_dir / "events.csv"),
            "experiment_assignments": pd.read_csv(sample_dir / "experiment_assignments.csv"),
            "interventions": pd.read_csv(sample_dir / "interventions.csv"),
            "labels": pd.read_csv(processed_dir / "labels.csv"),
        }

    print(f"Generating {args.count} users with seed {args.seed}")
    return generate_all_data(count=args.count, seed=args.seed, output_dir=args.data_dir)


def plot_precision_recall(
    y_true: pd.Series, y_prob: pd.Series, output_path: Path
) -> None:
    """Save a precision-recall curve plot."""
    from sklearn import metrics

    precision, recall, _ = metrics.precision_recall_curve(y_true, y_prob)
    pr_auc = metrics.average_precision_score(y_true, y_prob)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(recall, precision, label=f"PR-AUC = {pr_auc:.4f}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve (Test Set)")
    ax.legend(loc="lower left")
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_roc_curve(y_true: pd.Series, y_prob: pd.Series, output_path: Path) -> None:
    """Save an ROC curve plot."""
    from sklearn import metrics

    fpr, tpr, _ = metrics.roc_curve(y_true, y_prob)
    roc_auc = metrics.roc_auc_score(y_true, y_prob)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, label=f"ROC-AUC = {roc_auc:.4f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve (Test Set)")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_calibration(
    y_true: np.ndarray, y_prob: np.ndarray, output_path: Path
) -> None:
    """Save a reliability diagram."""
    calibration = compute_calibration_data(y_true, y_prob)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfectly calibrated")
    ax.plot(
        calibration["mean_predicted"],
        calibration["mean_observed"],
        marker="o",
        label="Model",
    )
    ax.set_xlabel("Mean Predicted Probability")
    ax.set_ylabel("Fraction of Positives")
    ax.set_title("Reliability Diagram (Test Set)")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_feature_importance(importance_df: pd.DataFrame, output_path: Path) -> None:
    """Save a horizontal bar plot of the top feature importances."""
    top_n = min(20, len(importance_df))
    top_features = importance_df.head(top_n).sort_values(by="importance_mean")

    fig, ax = plt.subplots(figsize=(7, 8))
    ax.barh(
        top_features["feature"],
        top_features["importance_mean"],
        xerr=top_features.get("importance_std", 0),
    )
    ax.set_xlabel("Permutation Importance (PR-AUC)")
    ax.set_title("Top Feature Importances (Validation Set)")
    ax.grid(True, axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> int:
    """Run the full churn-model training pipeline."""
    args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_dir = output_dir / PLOT_DIR
    plot_dir.mkdir(parents=True, exist_ok=True)

    data = ensure_data(args)
    users = data["users"]
    events = data["events"]
    labels = data["labels"]
    experiment_assignments = data["experiment_assignments"]

    print("Building pre-cutoff features and attaching labels...")
    model_matrix = prepare_model_matrix(users, events, labels, experiment_assignments)
    print(f"Model matrix shape: {model_matrix.shape}")
    print(f"Churn rate: {model_matrix['is_churned'].mean():.2%}")

    train_users, val_users, test_users, train_labels, val_labels, test_labels = (
        split_users_and_labels(users, labels)
    )

    train_df = model_matrix[
        model_matrix["user_id"].isin(train_users["user_id"])
    ].reset_index(drop=True)
    val_df = model_matrix[
        model_matrix["user_id"].isin(val_users["user_id"])
    ].reset_index(drop=True)
    test_df = model_matrix[
        model_matrix["user_id"].isin(test_users["user_id"])
    ].reset_index(drop=True)

    print(
        f"Train/Val/Test sizes: {len(train_df)} / {len(val_df)} / {len(test_df)}"
    )

    result = train_and_select_model(
        train_df,
        val_df,
        test_df,
        threshold_criterion=args.threshold_criterion,
        random_state=args.seed,
    )

    print(f"Selected model: {result.model_name}")
    print(f"Validation metrics: {result.val_metrics}")
    print(f"Test metrics: {result.test_metrics}")

    # Save artifacts
    model_path = output_dir / "churn_model.joblib"
    save_model(result, str(model_path))
    print(f"Saved model to {model_path}")

    metadata = {
        "model_name": result.model_name,
        "threshold": result.threshold,
        "threshold_criterion": args.threshold_criterion,
        "feature_columns": result.feature_columns,
        "train_size": len(train_df),
        "val_size": len(val_df),
        "test_size": len(test_df),
        "churn_rate": float(model_matrix["is_churned"].mean()),
        "random_seed": args.seed,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(output_dir / "model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    metrics_payload = {
        "validation": result.val_metrics,
        "test": result.test_metrics,
    }
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    feature_schema = {
        "categorical_features": [
            c for c in result.feature_columns if c in metadata["feature_columns"]
        ],
        "numeric_features": [
            c for c in result.feature_columns if c in metadata["feature_columns"]
        ],
    }
    with open(output_dir / "feature_schema.json", "w", encoding="utf-8") as f:
        json.dump(feature_schema, f, indent=2)

    # Explainability
    explainability: dict[str, list[dict[str, float]]] = {}
    if result.model_name == "logistic_regression":
        coef_df = extract_logistic_coefficients(result.model)
        explainability["logistic_coefficients"] = coef_df.head(20).to_dict(
            orient="records"
        )
        coef_df.to_csv(output_dir / "logistic_coefficients.csv", index=False)

    X_val = val_df[result.feature_columns]
    perm_importance = compute_permutation_importance(
        result.model, X_val, val_df["is_churned"].to_numpy(), random_state=args.seed
    )
    explainability["permutation_importance"] = perm_importance.head(20).to_dict(
        orient="records"
    )
    perm_importance.to_csv(output_dir / "permutation_importance.csv", index=False)

    with open(output_dir / "explainability.json", "w", encoding="utf-8") as f:
        json.dump(explainability, f, indent=2)

    # Plots
    y_test = test_df["is_churned"]
    plot_precision_recall(y_test, result.test_probabilities, plot_dir / "pr_curve.png")
    plot_roc_curve(y_test, result.test_probabilities, plot_dir / "roc_curve.png")
    plot_calibration(y_test.to_numpy(), result.test_probabilities, plot_dir / "calibration.png")
    plot_feature_importance(perm_importance, plot_dir / "feature_importance.png")

    print(f"Saved plots to {plot_dir}")
    print("Training complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
