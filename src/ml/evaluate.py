import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # needed for Mac to save charts without a display window
import matplotlib.pyplot as plt
import shap
import joblib
import os
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)
os.makedirs("documents/shap_charts", exist_ok=True)


def load_artifacts():
    """Load everything saved during training."""
    model = joblib.load("models/lgbm_model.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    return model, feature_names


def compute_shap_values(model, X_sample: pd.DataFrame):
    """
    Compute SHAP values for a sample of the data.
    We use a sample of 500 rows to keep it fast.
    SHAP values tell us how much each feature pushed
    the prediction up or down from the average.
    """
    logger.info("Computing SHAP values...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    # LightGBM returns list of [class_0, class_1] — we want class 1 (default)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    logger.info(f"SHAP values computed. Shape: {shap_values.shape}")
    return explainer, shap_values


def plot_shap_summary(shap_values, X_sample: pd.DataFrame):
    """
    Chart 1 — Summary plot showing which features matter most overall.
    Each dot is one applicant. Red = high feature value, Blue = low.
    """
    plt.figure(figsize=(10, 8))
    shap.summary_plot(
        shap_values,
        X_sample,
        plot_type="dot",
        show=False,
        max_display=15
    )
    plt.title("SHAP Feature Importance — Impact on Default Prediction", fontsize=13)
    plt.tight_layout()
    plt.savefig("documents/shap_charts/shap_summary.png", dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("Saved shap_summary.png")


def plot_shap_bar(shap_values, X_sample: pd.DataFrame):
    """
    Chart 2 — Bar chart of mean absolute SHAP values.
    Simple ranking of which features drive predictions the most.
    """
    plt.figure(figsize=(10, 7))
    shap.summary_plot(
        shap_values,
        X_sample,
        plot_type="bar",
        show=False,
        max_display=15
    )
    plt.title("Mean |SHAP Value| — Overall Feature Importance", fontsize=13)
    plt.tight_layout()
    plt.savefig("documents/shap_charts/shap_bar.png", dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("Saved shap_bar.png")


def explain_single_prediction(model, explainer, input_df: pd.DataFrame, index: int = 0):
    """
    Explain one individual prediction.
    Returns the top features that pushed the risk up or down.
    This is what we show in the UI for each applicant.
    """
    shap_values = explainer.shap_values(input_df)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    # Get the SHAP values for this one person
    single_shap = shap_values[index]
    feature_names = input_df.columns.tolist()

    # Build explanation dataframe
    explanation = pd.DataFrame({
        "feature": feature_names,
        "shap_value": single_shap,
        "feature_value": input_df.iloc[index].values
    })

    explanation["abs_shap"] = explanation["shap_value"].abs()
    explanation = explanation.sort_values("abs_shap", ascending=False).head(10)
    explanation["direction"] = explanation["shap_value"].apply(
        lambda x: "Increases Risk" if x > 0 else "Decreases Risk"
    )

    return explanation


def plot_single_explanation(explanation: pd.DataFrame, save_path: str = None):
    """
    Bar chart for a single applicant's SHAP explanation.
    Red bars = features that increased risk
    Green bars = features that decreased risk
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    colors = ["#e74c3c" if v > 0 else "#2ecc71" for v in explanation["shap_value"]]
    bars = ax.barh(
        explanation["feature"],
        explanation["shap_value"],
        color=colors,
        edgecolor="white"
    )

    ax.axvline(x=0, color="black", linewidth=0.8)
    ax.set_title("Why this prediction? — SHAP Explanation", fontsize=13, fontweight="bold")
    ax.set_xlabel("SHAP Value (positive = increases default risk)")

    # Add value labels
    for bar, val in zip(bars, explanation["shap_value"]):
        ax.text(
            bar.get_width() + 0.001,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}",
            va="center", fontsize=9
        )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved explanation chart to {save_path}")
    else:
        return fig


def run_shap_analysis():
    """
    Run full SHAP analysis on a sample of the test data.
    Saves summary charts and prints a sample explanation.
    """
    from src.data.loader import load_and_join_all
    from src.data.preprocessor import run_full_preprocessing, get_feature_target_split
    from sklearn.model_selection import train_test_split

    logger.info("Loading data for SHAP analysis...")
    df = load_and_join_all()
    df_clean = run_full_preprocessing(df, encoder_path="models/encoders.pkl")
    X, y = get_feature_target_split(df_clean)

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Use 300 rows for SHAP — full dataset would be very slow
    X_sample = X_test.sample(300, random_state=42)
    logger.info(f"Using {len(X_sample)} samples for SHAP analysis")

    model, feature_names = load_artifacts()
    explainer, shap_values = compute_shap_values(model, X_sample)

    plot_shap_summary(shap_values, X_sample)
    plot_shap_bar(shap_values, X_sample)

    # Show explanation for first applicant in sample
    logger.info("Generating single applicant explanation...")
    explanation = explain_single_prediction(model, explainer, X_sample, index=0)

    print("\n" + "="*60)
    print("   SAMPLE EXPLANATION — Applicant #1")
    print("="*60)
    print(explanation[["feature", "feature_value", "shap_value", "direction"]].to_string(index=False))
    print("="*60)

    logger.info("SHAP analysis complete!")


if __name__ == "__main__":
    run_shap_analysis()