import pandas as pd
import numpy as np
import joblib
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_model_artifacts():
    """Load model, encoders and feature names from disk."""
    model = joblib.load("models/lgbm_model.pkl")
    encoders = joblib.load("models/encoders.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    logger.info("Loaded model artifacts")
    return model, encoders, feature_names


def assign_risk_band(probability: float) -> str:
    """
    Convert a probability into a human-readable risk band.
    Low / Medium / High
    """
    if probability < 0.3:
        return "Low"
    elif probability < 0.6:
        return "Medium"
    else:
        return "High"


def preprocess_single_input(input_dict: dict, encoders: dict, feature_names: list) -> pd.DataFrame:
    """
    Take a single applicant's data (as a dict from the UI form),
    clean it, and return a dataframe ready for prediction.
    """
    df = pd.DataFrame([input_dict])

    # Apply label encoders to categorical columns
    for col, encoder in encoders.items():
        if col in df.columns:
            val = str(df[col].iloc[0])
            if val in encoder.classes_:
                df[col] = encoder.transform([val])
            else:
                df[col] = 0  # fallback for unseen categories

    # Add engineered features
    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / (df["AMT_INCOME_TOTAL"] + 1)

    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_INCOME_RATIO"] = df["AMT_ANNUITY"] / (df["AMT_INCOME_TOTAL"] + 1)

    if "AMT_CREDIT" in df.columns and "AMT_GOODS_PRICE" in df.columns:
        df["CREDIT_GOODS_RATIO"] = df["AMT_CREDIT"] / (df["AMT_GOODS_PRICE"] + 1)

    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = abs(df["DAYS_BIRTH"]) / 365

    if "DAYS_EMPLOYED" in df.columns:
        df["YEARS_EMPLOYED"] = abs(df["DAYS_EMPLOYED"]) / 365

    # Add any missing columns with 0
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    # Keep only the columns the model was trained on, in the right order
    df = df[feature_names]
    return df


def predict_default(input_dict: dict) -> dict:
    """
    Main prediction function.
    Takes applicant data, returns risk score, band, and probability.
    """
    model, encoders, feature_names = load_model_artifacts()

    df_input = preprocess_single_input(input_dict, encoders, feature_names)

    probability = model.predict_proba(df_input)[0][1]
    risk_band = assign_risk_band(probability)
    risk_score = round(probability * 100, 1)

    result = {
        "probability": round(float(probability), 4),
        "risk_score": risk_score,
        "risk_band": risk_band,
    }

    logger.info(f"Prediction: {result}")
    return result