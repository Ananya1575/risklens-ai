import pandas as pd
import numpy as np
import joblib
import os
import json
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, classification_report,
    confusion_matrix, average_precision_score
)
from imblearn.over_sampling import SMOTE
from src.data.loader import load_and_join_all
from src.data.preprocessor import run_full_preprocessing, get_feature_target_split
from src.utils.logger import get_logger

logger = get_logger(__name__)

os.makedirs("models", exist_ok=True)


def get_class_weight_ratio(y):
    """
    Calculate how imbalanced the classes are.
    Example: if 90% are 0 and 10% are 1, ratio = 9.
    We pass this to LightGBM so it pays more attention to the minority class.
    """
    count_0 = (y == 0).sum()
    count_1 = (y == 1).sum()
    ratio = count_0 / count_1
    logger.info(f"Class imbalance ratio: {ratio:.2f} (used as scale_pos_weight)")
    return ratio


def train_model(X_train, y_train, scale_pos_weight):
    """
    Train a LightGBM classifier.

    Why LightGBM?
    - Very fast on large datasets
    - Handles missing values natively
    - Great performance on tabular/financial data
    - Used widely in real banking ML systems
    """
    model = LGBMClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        scale_pos_weight=scale_pos_weight,  # handles class imbalance
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )

    logger.info("Training LightGBM model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train)],
    )
    logger.info("Training complete!")
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance and return all metrics.
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)

    roc_auc = roc_auc_score(y_test, y_pred_proba)
    avg_precision = average_precision_score(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "roc_auc": round(roc_auc, 4),
        "avg_precision_score": round(avg_precision, 4),
        "precision_class_1": round(report["1"]["precision"], 4),
        "recall_class_1": round(report["1"]["recall"], 4),
        "f1_class_1": round(report["1"]["f1-score"], 4),
        "confusion_matrix": cm,
    }

    logger.info(f"ROC-AUC Score: {metrics['roc_auc']}")
    logger.info(f"Avg Precision Score: {metrics['avg_precision_score']}")
    logger.info(f"Precision (default class): {metrics['precision_class_1']}")
    logger.info(f"Recall (default class): {metrics['recall_class_1']}")
    logger.info(f"F1 (default class): {metrics['f1_class_1']}")

    return metrics


def get_feature_importance(model, feature_names, top_n=20):
    """
    Get the top N most important features the model used.
    """
    importance = model.feature_importances_
    feat_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    }).sort_values("importance", ascending=False).head(top_n)

    logger.info(f"Top 5 features: {feat_df['feature'].head(5).tolist()}")
    return feat_df


def run_training_pipeline():
    """
    Master function — runs the full training pipeline end to end.
    """
    logger.info("=== STARTING TRAINING PIPELINE ===")

    # Step 1 — Load and preprocess data
    df = load_and_join_all()
    df_clean = run_full_preprocessing(df, encoder_path="models/encoders.pkl")
    X, y = get_feature_target_split(df_clean)

    # Step 2 — Train/test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

    # Step 3 — Handle class imbalance using scale_pos_weight
    scale_pos_weight = get_class_weight_ratio(y_train)

    # Step 4 — Train model
    model = train_model(X_train, y_train, scale_pos_weight)

    # Step 5 — Evaluate
    metrics = evaluate_model(model, X_test, y_test)

    # Step 6 — Feature importance
    feat_importance = get_feature_importance(model, X.columns.tolist())

    # Step 7 — Save everything to disk
    joblib.dump(model, "models/lgbm_model.pkl")
    logger.info("Saved model to models/lgbm_model.pkl")

    feat_importance.to_csv("models/feature_importance.csv", index=False)
    logger.info("Saved feature importance to models/feature_importance.csv")

    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info("Saved metrics to models/metrics.json")

    # Save feature names for prediction later
    joblib.dump(X.columns.tolist(), "models/feature_names.pkl")
    logger.info("Saved feature names to models/feature_names.pkl")

    logger.info("=== TRAINING PIPELINE COMPLETE ===")
    return model, metrics, feat_importance


if __name__ == "__main__":
    model, metrics, feat_importance = run_training_pipeline()

    print("\n" + "="*50)
    print("         FINAL MODEL METRICS")
    print("="*50)
    print(f"  ROC-AUC Score       : {metrics['roc_auc']}")
    print(f"  Avg Precision Score : {metrics['avg_precision_score']}")
    print(f"  Precision (default) : {metrics['precision_class_1']}")
    print(f"  Recall (default)    : {metrics['recall_class_1']}")
    print(f"  F1 (default)        : {metrics['f1_class_1']}")
    print("="*50)
    print("\nTop 10 most important features:")
    print(feat_importance.head(10).to_string(index=False))