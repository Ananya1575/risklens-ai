import streamlit as st
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#f25c5c;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Module 06</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">Model Metrics</h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">LightGBM evaluation results on the 20% held-out test set (61,503 applicants).</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    try:
        with open("models/metrics.json") as f:
            metrics = json.load(f)

        # KPI row
        kpis = [
            ("ROC-AUC", metrics["roc_auc"], "#4f8ef7", "Area under ROC curve"),
            ("Avg Precision", metrics["avg_precision_score"], "#7c5cfc", "PR-AUC score"),
            ("Recall", metrics["recall_class_1"], "#22c87a", "Default class recall"),
            ("F1 Score", metrics["f1_class_1"], "#f5a623", "Default class F1"),
        ]

        cols = st.columns(4)
        for col, (label, val, color, sub) in zip(cols, kpis):
            with col:
                st.markdown(f"""
                <div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1.25rem;border-top:3px solid {color};text-align:center;">
                    <div style="font-size:0.68rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">{label}</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:{color};">{val}</div>
                    <div style="font-size:0.7rem;color:#6b7280;margin-top:4px;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:0.95rem;font-weight:700;color:#e8eaf0;margin-bottom:0.75rem;">Confusion Matrix</p>', unsafe_allow_html=True)
            cm = np.array(metrics["confusion_matrix"])
            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_facecolor('#111318')
            ax.set_facecolor('#111318')
            sns.heatmap(
                cm, annot=True, fmt="d", ax=ax,
                cmap=sns.light_palette("#4f8ef7", as_cmap=True),
                xticklabels=["No Default", "Default"],
                yticklabels=["No Default", "Default"],
                linewidths=0.5, linecolor="#1f2330",
                annot_kws={"size": 12, "color": "#e8eaf0", "weight": "bold"}
            )
            ax.set_xlabel("Predicted", color="#6b7280", fontsize=9)
            ax.set_ylabel("Actual", color="#6b7280", fontsize=9)
            ax.tick_params(colors="#9ca3af", labelsize=9)
            ax.set_title("Test Set Confusion Matrix", color="#9ca3af", fontsize=10, pad=10)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:0.95rem;font-weight:700;color:#e8eaf0;margin-bottom:0.75rem;">Top 15 Feature Importances</p>', unsafe_allow_html=True)
            feat_df = pd.read_csv("models/feature_importance.csv").head(15)
            fig, ax = plt.subplots(figsize=(5, 5))
            fig.patch.set_facecolor('#111318')
            ax.set_facecolor('#111318')
            colors_bar = ["#4f8ef7" if i < 3 else "#1f3a6e" for i in range(len(feat_df))]
            ax.barh(feat_df["feature"], feat_df["importance"], color=colors_bar, height=0.65)
            ax.invert_yaxis()
            ax.set_xlabel("Importance Score", color="#6b7280", fontsize=9)
            ax.tick_params(colors="#9ca3af", labelsize=8)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_color("#1f2330")
            ax.spines["left"].set_color("#1f2330")
            ax.set_title("LightGBM Feature Importance", color="#9ca3af", fontsize=10, pad=10)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        st.markdown('<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:0.95rem;font-weight:700;color:#e8eaf0;margin-bottom:0.75rem;">Model Configuration</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        config_items = [
            ("Algorithm", "LightGBM (LGBM Classifier)"),
            ("Estimators", "500 trees"),
            ("Learning Rate", "0.05"),
            ("Max Depth", "6"),
            ("Imbalance Strategy", "scale_pos_weight = 11.39"),
            ("Train/Test Split", "80% / 20% stratified"),
            ("Features", "86 (after preprocessing)"),
            ("Training Samples", "246,008"),
        ]
        for i, (k, v) in enumerate(config_items):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.6rem 0;border-bottom:1px solid #1f2330;">
                    <span style="font-size:0.82rem;color:#6b7280;">{k}</span>
                    <span style="font-size:0.82rem;color:#e8eaf0;font-family:'JetBrains Mono',monospace;">{v}</span>
                </div>
                """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("metrics.json not found. Run `src/ml/train.py` first.")