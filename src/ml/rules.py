import pandas as pd
import numpy as np
import joblib
import json
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ── Hard business rules derived from EDA + model insights ──────────────────
# These are human-readable policy rules a credit officer can act on directly.
# Each rule has: condition, risk_level, reason, and recommended_action.

BUSINESS_RULES = [
    {
        "rule_id": "R01",
        "name": "Young Applicant High Risk",
        "condition": "Age < 25 years",
        "risk_level": "High",
        "reason": "Applicants under 25 default at 12.3% — 52% above the 8.07% average.",
        "recommended_action": "Require co-signer or additional collateral.",
        "color": "#f25c5c",
    },
    {
        "rule_id": "R02",
        "name": "Low External Credit Score",
        "condition": "EXT_SOURCE_2 < 0.3 AND EXT_SOURCE_3 < 0.3",
        "risk_level": "High",
        "reason": "External credit scores are the top 2 model predictors. Combined low scores strongly indicate default risk.",
        "recommended_action": "Reject or escalate to senior credit officer.",
        "color": "#f25c5c",
    },
    {
        "rule_id": "R03",
        "name": "Excessive Credit-to-Income Ratio",
        "condition": "AMT_CREDIT > 5 × AMT_INCOME_TOTAL",
        "risk_level": "High",
        "reason": "Credit exceeding 5× annual income indicates severe over-leveraging.",
        "recommended_action": "Reduce approved credit amount or reject.",
        "color": "#f25c5c",
    },
    {
        "rule_id": "R04",
        "name": "High-Risk Occupation",
        "condition": "OCCUPATION_TYPE in [Low-skill Laborers, Drivers, Waiters/barmen staff]",
        "risk_level": "High",
        "reason": "These occupations show 13–17% default rates — well above average.",
        "recommended_action": "Apply stricter income verification and limit credit amount.",
        "color": "#f25c5c",
    },
    {
        "rule_id": "R05",
        "name": "Multiple Prior Refusals",
        "condition": "prev_refused_count >= 2",
        "risk_level": "High",
        "reason": "Two or more prior refusals at Home Credit indicate persistent creditworthiness issues.",
        "recommended_action": "Reject unless strong compensating factors exist.",
        "color": "#f25c5c",
    },
    {
        "rule_id": "R06",
        "name": "Moderate Credit-to-Income",
        "condition": "AMT_CREDIT between 3× and 5× AMT_INCOME_TOTAL",
        "risk_level": "Medium",
        "reason": "Elevated leverage increases repayment burden but is not extreme.",
        "recommended_action": "Manual review — verify income stability and employment.",
        "color": "#f5a623",
    },
    {
        "rule_id": "R07",
        "name": "Cash Loan Contract",
        "condition": "NAME_CONTRACT_TYPE = 'Cash loans'",
        "risk_level": "Medium",
        "reason": "Cash loans default at 8.3% vs 5.5% for revolving loans — 51% higher risk.",
        "recommended_action": "Apply standard due diligence. Consider lower initial credit limit.",
        "color": "#f5a623",
    },
    {
        "rule_id": "R08",
        "name": "Short Employment History",
        "condition": "YEARS_EMPLOYED < 1",
        "risk_level": "Medium",
        "reason": "Less than 1 year of employment indicates income instability.",
        "recommended_action": "Request employment verification letter and 3-month bank statements.",
        "color": "#f5a623",
    },
    {
        "rule_id": "R09",
        "name": "Strong Credit Profile",
        "condition": "EXT_SOURCE_2 > 0.6 AND EXT_SOURCE_3 > 0.6 AND Age > 35",
        "risk_level": "Low",
        "reason": "High bureau scores combined with mature age profile. Historically low default rate.",
        "recommended_action": "Approve with standard terms.",
        "color": "#22c87a",
    },
    {
        "rule_id": "R10",
        "name": "Conservative Borrowing",
        "condition": "AMT_CREDIT < 1.5 × AMT_INCOME_TOTAL AND YEARS_EMPLOYED > 3",
        "risk_level": "Low",
        "reason": "Low leverage with stable employment — strongest low-risk signal combination.",
        "recommended_action": "Approve. May qualify for preferred interest rate.",
        "color": "#22c87a",
    },
]


def evaluate_rules_for_applicant(input_dict: dict) -> list:
    """
    Evaluate which business rules fire for a given applicant.
    Returns list of triggered rules.
    """
    triggered = []

    age = abs(input_dict.get("DAYS_BIRTH", -35 * 365)) / 365
    ext2 = input_dict.get("EXT_SOURCE_2", 0.5)
    ext3 = input_dict.get("EXT_SOURCE_3", 0.5)
    income = input_dict.get("AMT_INCOME_TOTAL", 150000)
    credit = input_dict.get("AMT_CREDIT", 300000)
    years_emp = abs(input_dict.get("DAYS_EMPLOYED", -1825)) / 365
    occupation = input_dict.get("OCCUPATION_TYPE", "")
    contract = input_dict.get("NAME_CONTRACT_TYPE", "")
    prev_refused = input_dict.get("prev_refused_count", 0)

    credit_income_ratio = credit / (income + 1)
    high_risk_occupations = ["Low-skill Laborers", "Drivers", "Waiters/barmen staff"]

    checks = {
        "R01": age < 25,
        "R02": ext2 < 0.3 and ext3 < 0.3,
        "R03": credit_income_ratio > 5,
        "R04": occupation in high_risk_occupations,
        "R05": prev_refused >= 2,
        "R06": 3 < credit_income_ratio <= 5,
        "R07": contract == "Cash loans",
        "R08": years_emp < 1,
        "R09": ext2 > 0.6 and ext3 > 0.6 and age > 35,
        "R10": credit_income_ratio < 1.5 and years_emp > 3,
    }

    for rule in BUSINESS_RULES:
        if checks.get(rule["rule_id"], False):
            triggered.append(rule)

    return triggered


def get_all_rules() -> list:
    """Return all business rules for display in the UI."""
    return BUSINESS_RULES


def get_rules_summary() -> dict:
    """Return count of rules by risk level."""
    high = sum(1 for r in BUSINESS_RULES if r["risk_level"] == "High")
    medium = sum(1 for r in BUSINESS_RULES if r["risk_level"] == "Medium")
    low = sum(1 for r in BUSINESS_RULES if r["risk_level"] == "Low")
    return {"high": high, "medium": medium, "low": low, "total": len(BUSINESS_RULES)}