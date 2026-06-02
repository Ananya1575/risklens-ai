import streamlit as st
import os
from PIL import Image

def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#4f8ef7;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Module 01</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">EDA Dashboard</h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">Visual exploration of the Home Credit dataset — 307,511 applicants, 122 raw features.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    charts_dir = "documents/eda_charts"

    chart_data = [
        ("01_target_distribution.png", "Loan Default Distribution",
         "8.07%", "Default Rate",
         "91.9% of applicants do not default. This 11:1 imbalance is the core challenge for the ML model — handled using scale_pos_weight in LightGBM rather than resampling, which preserves data integrity."),
        ("02_age_vs_default.png", "Default Rate by Age Group",
         "12.3%", "Age 20–25 Default",
         "Clear inverse relationship between age and default risk. Youngest cohort defaults at 12.3% — 2.5× the rate of applicants over 60 (4.9%). Age is a significant risk signal."),
        ("03_income_vs_default.png", "Income Distribution",
         "~$166K", "Avg Defaulter Income",
         "Defaulters earn slightly less on average ($165,612 vs $169,078) but the distributions heavily overlap. Income alone is a weak predictor — combined ratios perform much better."),
        ("04_contract_type.png", "Default Rate by Contract Type",
         "8.3%", "Cash Loan Default",
         "Cash loans default at 8.3% vs 5.5% for revolving loans — a 51% higher risk. Cash loan applicants should face stricter underwriting criteria."),
        ("05_credit_income_ratio.png", "Credit-to-Income Ratio",
         "2×", "Median Ratio (Both Groups)",
         "Both groups peak around 2× income ratio. Defaulters show a heavier right tail at high ratios (8–12×), confirming over-leveraging as a risk factor."),
        ("06_missing_values.png", "Missing Value Analysis",
         "60–70%", "Property Column Missingness",
         "Property-related columns (floor count, living area) have 60–70% missing data and were dropped. OWN_CAR_AGE at 66% missing was also excluded from training."),
    ]

    for i, (filename, title, stat_val, stat_label, insight) in enumerate(chart_data):
        path = os.path.join(charts_dir, filename)

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
            <div style="width:24px;height:24px;background:#4f8ef7;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;color:#fff;font-family:'Syne',sans-serif;">{i+1:02d}</div>
            <h3 style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:#e8eaf0;margin:0;">{title}</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            if os.path.exists(path):
                img = Image.open(path)
                st.image(img, use_container_width=True)
            else:
                st.warning(f"Run `notebooks/eda.py` to generate this chart.")

        with col2:
            st.markdown(f"""
            <div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1.25rem;margin-bottom:0.75rem;border-top:3px solid #4f8ef7;">
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#4f8ef7;">{stat_val}</div>
                <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;margin-top:2px;">{stat_label}</div>
            </div>
            <div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1.25rem;">
                <div style="font-size:0.7rem;color:#4f8ef7;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:0.5rem;">Business Insight</div>
                <div style="font-size:0.82rem;color:#9ca3af;line-height:1.65;">{insight}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>', unsafe_allow_html=True)