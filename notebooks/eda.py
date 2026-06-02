import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

from src.data.loader import load_and_join_all
from src.data.preprocessor import run_full_preprocessing
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Create folder to save charts
os.makedirs("documents/eda_charts", exist_ok=True)


def plot_target_distribution(df_raw):
    """Chart 1 — How many defaulters vs non-defaulters."""
    counts = df_raw["TARGET"].value_counts()
    labels = ["No Default (0)", "Default (1)"]
    colors = ["#2ecc71", "#e74c3c"]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, counts.values, color=colors, edgecolor="white", linewidth=1.5)

    for bar, count in zip(bars, counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2000,
            f"{count:,}\n({count/counts.sum()*100:.1f}%)",
            ha="center", va="bottom", fontsize=11
        )

    ax.set_title("Loan Default Distribution", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Applicants")
    ax.set_ylim(0, counts.max() * 1.2)
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/01_target_distribution.png", dpi=150)
    plt.close()
    logger.info("Saved chart 01_target_distribution.png")


def plot_age_vs_default(df_raw):
    """Chart 2 — Does age affect default rate?"""
    df = df_raw.copy()
    df["AGE_YEARS"] = df["DAYS_BIRTH"].abs() / 365
    df["AGE_GROUP"] = pd.cut(
        df["AGE_YEARS"],
        bins=[20, 25, 30, 35, 40, 50, 60, 70],
        labels=["20-25", "25-30", "30-35", "35-40", "40-50", "50-60", "60-70"]
    )

    age_default = df.groupby("AGE_GROUP", observed=True)["TARGET"].mean() * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(
        age_default.index.astype(str),
        age_default.values,
        color="#3498db", edgecolor="white", linewidth=1.5
    )

    for bar, val in zip(bars, age_default.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{val:.1f}%",
            ha="center", va="bottom", fontsize=10
        )

    ax.set_title("Default Rate by Age Group", fontsize=14, fontweight="bold")
    ax.set_xlabel("Age Group (Years)")
    ax.set_ylabel("Default Rate (%)")
    ax.axhline(y=df_raw["TARGET"].mean() * 100, color="red",
               linestyle="--", linewidth=1.5, label="Overall average")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/02_age_vs_default.png", dpi=150)
    plt.close()
    logger.info("Saved chart 02_age_vs_default.png")


def plot_income_vs_default(df_raw):
    """Chart 3 — Income distribution for defaulters vs non-defaulters."""
    df = df_raw.copy()
    # Cap income at 99th percentile to remove extreme outliers
    cap = df["AMT_INCOME_TOTAL"].quantile(0.99)
    df = df[df["AMT_INCOME_TOTAL"] <= cap]

    fig, ax = plt.subplots(figsize=(9, 5))
    for target, color, label in [(0, "#2ecc71", "No Default"), (1, "#e74c3c", "Default")]:
        subset = df[df["TARGET"] == target]["AMT_INCOME_TOTAL"]
        ax.hist(subset, bins=50, alpha=0.6, color=color, label=label, density=True)

    ax.set_title("Income Distribution — Default vs No Default", fontsize=14, fontweight="bold")
    ax.set_xlabel("Annual Income")
    ax.set_ylabel("Density")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/03_income_vs_default.png", dpi=150)
    plt.close()
    logger.info("Saved chart 03_income_vs_default.png")


def plot_contract_type(df_raw):
    """Chart 4 — Default rate by loan contract type."""
    contract_default = df_raw.groupby("NAME_CONTRACT_TYPE")["TARGET"].mean() * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(
        contract_default.index,
        contract_default.values,
        color=["#9b59b6", "#f39c12"],
        edgecolor="white", linewidth=1.5
    )

    for bar, val in zip(bars, contract_default.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{val:.1f}%",
            ha="center", va="bottom", fontsize=11
        )

    ax.set_title("Default Rate by Contract Type", fontsize=14, fontweight="bold")
    ax.set_ylabel("Default Rate (%)")
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/04_contract_type.png", dpi=150)
    plt.close()
    logger.info("Saved chart 04_contract_type.png")


def plot_credit_income_ratio(df_raw):
    """Chart 5 — Credit to income ratio for defaulters vs non-defaulters."""
    df = df_raw.copy()
    df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / (df["AMT_INCOME_TOTAL"] + 1)
    cap = df["CREDIT_INCOME_RATIO"].quantile(0.99)
    df = df[df["CREDIT_INCOME_RATIO"] <= cap]

    fig, ax = plt.subplots(figsize=(9, 5))
    for target, color, label in [(0, "#2ecc71", "No Default"), (1, "#e74c3c", "Default")]:
        subset = df[df["TARGET"] == target]["CREDIT_INCOME_RATIO"]
        ax.hist(subset, bins=50, alpha=0.6, color=color, label=label, density=True)

    ax.set_title("Credit-to-Income Ratio — Default vs No Default", fontsize=14, fontweight="bold")
    ax.set_xlabel("Credit / Annual Income")
    ax.set_ylabel("Density")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/05_credit_income_ratio.png", dpi=150)
    plt.close()
    logger.info("Saved chart 05_credit_income_ratio.png")


def plot_missing_values(df_raw):
    """Chart 6 — Top 20 columns with most missing values."""
    missing = df_raw.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False).head(20)
    missing_pct = (missing / len(df_raw) * 100)

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(missing_pct.index, missing_pct.values, color="#e67e22")
    ax.set_title("Top 20 Columns by Missing Value %", fontsize=14, fontweight="bold")
    ax.set_xlabel("Missing (%)")
    ax.axvline(x=45, color="red", linestyle="--", linewidth=1.5, label="Drop threshold (45%)")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.savefig("documents/eda_charts/06_missing_values.png", dpi=150)
    plt.close()
    logger.info("Saved chart 06_missing_values.png")


def print_business_insights(df_raw):
    """Print 5 key business insights from the data."""

    df = df_raw.copy()
    df["AGE_YEARS"] = df["DAYS_BIRTH"].abs() / 365
    df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / (df["AMT_INCOME_TOTAL"] + 1)

    print("\n" + "="*60)
    print("         BUSINESS INSIGHTS FROM EDA")
    print("="*60)

    # Insight 1
    default_rate = df["TARGET"].mean() * 100
    print(f"\n1. OVERALL DEFAULT RATE: {default_rate:.2f}%")
    print("   Only 8% of applicants default — heavily imbalanced dataset.")
    print("   We must handle this imbalance carefully in the ML model.")

    # Insight 2
    young = df[df["AGE_YEARS"] < 30]["TARGET"].mean() * 100
    old = df[df["AGE_YEARS"] > 50]["TARGET"].mean() * 100
    print(f"\n2. AGE RISK: Young applicants (<30) default at {young:.1f}%")
    print(f"   vs older applicants (>50) at {old:.1f}%")
    print("   Younger applicants are significantly higher risk.")

    # Insight 3
    contract_rates = df.groupby("NAME_CONTRACT_TYPE")["TARGET"].mean() * 100
    print(f"\n3. CONTRACT TYPE RISK:")
    for contract, rate in contract_rates.items():
        print(f"   {contract}: {rate:.1f}% default rate")

    # Insight 4
    high_ratio = df[df["CREDIT_INCOME_RATIO"] > 3]["TARGET"].mean() * 100
    low_ratio = df[df["CREDIT_INCOME_RATIO"] <= 1]["TARGET"].mean() * 100
    print(f"\n4. CREDIT-TO-INCOME RATIO MATTERS:")
    print(f"   Applicants with credit > 3x income default at {high_ratio:.1f}%")
    print(f"   Applicants with credit <= 1x income default at {low_ratio:.1f}%")

    # Insight 5
    gender_rates = df.groupby("CODE_GENDER")["TARGET"].mean() * 100
    print(f"\n5. GENDER BREAKDOWN:")
    for gender, rate in gender_rates.items():
        print(f"   {gender}: {rate:.1f}% default rate")

    print("\n" + "="*60)


def run_eda():
    """Run all EDA steps."""
    logger.info("Loading raw data for EDA...")
    df_raw = pd.read_csv("data/application_train.csv")
    logger.info(f"Loaded {df_raw.shape[0]} rows for EDA")

    logger.info("Generating charts...")
    plot_target_distribution(df_raw)
    plot_age_vs_default(df_raw)
    plot_income_vs_default(df_raw)
    plot_contract_type(df_raw)
    plot_credit_income_ratio(df_raw)
    plot_missing_values(df_raw)

    print_business_insights(df_raw)
    logger.info("EDA complete! Charts saved to documents/eda_charts/")


if __name__ == "__main__":
    run_eda()