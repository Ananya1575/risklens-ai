import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
import os
from PIL import Image


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#22c87a;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Module 04</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">Explainable AI</h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">SHAP values explain why the model made each prediction — globally and per applicant.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;color:#e8eaf0;margin-bottom:0.25rem;">Global Feature Importance</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#6b7280;margin-bottom:1rem;">Computed over 300 test samples. Shows which features have the largest average impact on predictions.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    shap_dir = "documents/shap_charts"

    with col1:
        path = os.path.join(shap_dir, "shap_bar.png")
        if os.path.exists(path):
            st.markdown('<div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1rem;">', unsafe_allow_html=True)
            st.image(Image.open(path), caption="Mean |SHAP| — Feature Ranking", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        path = os.path.join(shap_dir, "shap_summary.png")
        if os.path.exists(path):
            st.markdown('<div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1rem;">', unsafe_allow_html=True)
            st.image(Image.open(path), caption="SHAP Dot Plot — Direction of Impact", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;color:#e8eaf0;margin-bottom:0.25rem;">Single Applicant Explanation</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#6b7280;margin-bottom:1rem;">Enter applicant details to see which features drove their specific risk score.</p>', unsafe_allow_html=True)

    with st.form("shap_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input("Annual Income", value=150000, step=5000)
            credit = st.number_input("Loan Amount", value=500000, step=10000)
        with col2:
            annuity = st.number_input("Monthly Annuity", value=25000, step=1000)
            goods_price = st.number_input("Goods Price", value=450000, step=10000)
        with col3:
            age_years = st.slider("Age (Years)", 18, 70, 35)
            ext_source_2 = st.slider("Ext Credit Score 2", 0.0, 1.0, 0.5, 0.01)
            ext_source_3 = st.slider("Ext Credit Score 3", 0.0, 1.0, 0.5, 0.01)

        submitted = st.form_submit_button("→  Generate Explanation", use_container_width=True)

    if submitted:
        with st.spinner("Computing SHAP values..."):
            try:
                from src.ml.evaluate import explain_single_prediction
                from src.ml.predict import preprocess_single_input, load_model_artifacts

                model, encoders, feature_names = load_model_artifacts()
                explainer = shap.TreeExplainer(model)

                input_data = {
                    "AMT_INCOME_TOTAL": income, "AMT_CREDIT": credit,
                    "AMT_ANNUITY": annuity, "AMT_GOODS_PRICE": goods_price,
                    "DAYS_BIRTH": -(age_years * 365), "DAYS_EMPLOYED": -1825,
                    "EXT_SOURCE_2": ext_source_2, "EXT_SOURCE_3": ext_source_3,
                }

                input_df = preprocess_single_input(input_data, encoders, feature_names)
                explanation = explain_single_prediction(model, explainer, input_df, index=0)

                st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

                fig, ax = plt.subplots(figsize=(10, 5))
                fig.patch.set_facecolor('#111318')
                ax.set_facecolor('#111318')
                colors = ["#f25c5c" if v > 0 else "#22c87a" for v in explanation["shap_value"]]
                bars = ax.barh(explanation["feature"], explanation["shap_value"], color=colors, height=0.6)
                ax.axvline(x=0, color="#1f2330", linewidth=1.5)
                ax.set_xlabel("SHAP Value", color="#6b7280", fontsize=9)
                ax.tick_params(colors="#9ca3af", labelsize=9)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_color("#1f2330")
                ax.spines["left"].set_color("#1f2330")
                ax.set_title("Feature Impact — Red increases risk · Green decreases risk", color="#9ca3af", fontsize=10, pad=12)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

                st.dataframe(
                    explanation[["feature", "feature_value", "shap_value", "direction"]].reset_index(drop=True),
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error: {e}")