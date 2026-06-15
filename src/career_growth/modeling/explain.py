"""Explainability helpers for churn models."""

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance


def extract_feature_names(pipeline, input_features: list[str] | None = None) -> list[str]:
    """Return the feature names produced by the pipeline preprocessor."""
    preprocessor = pipeline.named_steps["preprocessor"]
    try:
        feature_names = preprocessor.get_feature_names_out(input_features)
    except AttributeError:
        feature_names = np.array([f"feature_{i}" for i in range(preprocessor.transform(pd.DataFrame()).shape[1])])
    return [str(name) for name in feature_names]


def extract_logistic_coefficients(
    pipeline, input_features: list[str] | None = None
) -> pd.DataFrame:
    """Return a DataFrame of logistic-regression feature coefficients.

    The coefficients are returned sorted by absolute value in descending order.
    """
    feature_names = extract_feature_names(pipeline, input_features)
    classifier = pipeline.named_steps["classifier"]
    coefficients = classifier.coef_.flatten()

    df = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "abs_coefficient": np.abs(coefficients),
        }
    )
    return df.sort_values(by="abs_coefficient", ascending=False).reset_index(drop=True)


def compute_permutation_importance(
    pipeline,
    X: pd.DataFrame,
    y: np.ndarray,
    n_repeats: int = 10,
    random_state: int = 42,
) -> pd.DataFrame:
    """Compute permutation importance for any sklearn pipeline on a validation set.

    Returns a DataFrame with one row per input feature, sorted by mean importance.
    """
    result = permutation_importance(
        pipeline,
        X,
        y,
        n_repeats=n_repeats,
        random_state=random_state,
        scoring="average_precision",
        n_jobs=-1,
    )

    df = pd.DataFrame(
        {
            "feature": X.columns.tolist(),
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    )
    return df.sort_values(by="importance_mean", ascending=False).reset_index(drop=True)
