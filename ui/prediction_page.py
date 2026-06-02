import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#7c5cfc;letter-spacing:0.15em;
                    text-transform:uppercase;margin-bottom:0.5rem;">Module 03</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                   color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">
            Risk Assessment
        </h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">
            Enter applicant details once — get risk score, SHAP explanation,
            and triggered decision rules all in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>',
        unsafe_allow_html=True
    )

    with st.form("risk_assessment_form"):

        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-size:0.95rem;'
            'font-weight:700;color:#e8eaf0;margin-bottom:1rem;">'
            'Financial Information</p>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input(
                "Annual Income",
                min_value=10000, max_value=10000000,
                value=150000, step=5000
            )
            credit = st.number_input(
                "Loan Credit Amount",
                min_value=10000, max_value=5000000,
                value=500000, step=10000
            )
        with col2:
            annuity = st.number_input(
                "Monthly Annuity Payment",
                min_value=1000, max_value=200000,
                value=25000, step=1000
            )
            goods_price = st.number_input(
                "Goods Price",
                min_value=10000, max_value=5000000,
                value=450000, step=10000
            )
        with col3:
            ext_source_2 = st.slider(
                "External Credit Score 2", 0.0, 1.0, 0.5, 0.01
            )
            ext_source_3 = st.slider(
                "External Credit Score 3", 0.0, 1.0, 0.5, 0.01
            )

        st.markdown(
            '<div style="height:1px;background:#1f2330;margin:1rem 0;"></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-size:0.95rem;'
            'font-weight:700;color:#e8eaf0;margin-bottom:1rem;">'
            'Personal Information</p>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            age_years = st.slider("Age (Years)", min_value=18, max_value=70, value=35)
            years_employed = st.slider("Years Employed", min_value=0, max_value=40, value=5)
        with col2:
            gender = st.selectbox("Gender", ["M", "F"])
            contract_type = st.selectbox(
                "Contract Type", ["Cash loans", "Revolving loans"]
            )
        with col3:
            education = st.selectbox("Education Level", [
                "Higher education",
                "Secondary / secondary special",
                "Incomplete higher",
                "Lower secondary",
                "Academic degree"
            ])
            occupation = st.selectbox("Occupation Type", [
                "Laborers",
                "Core staff",
                "Accountants",
                "Managers",
                "Drivers",
                "Sales staff",
                "Cleaning staff",
                "Cooking staff",
                "Private service staff",
                "Medicine staff",
                "Security staff",
                "High skill tech staff",
                "Waiters/barmen staff",
                "Low-skill Laborers",
                "Secretaries",
                "IT staff",
                "HR staff",
                "Realty agents"
            ])

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "→  Run Full Risk Assessment", use_container_width=True
        )

    if submitted:
        input_data = {
            "AMT_INCOME_TOTAL": income,
            "AMT_CREDIT": credit,
            "AMT_ANNUITY": annuity,
            "AMT_GOODS_PRICE": goods_price,
            "DAYS_BIRTH": -(age_years * 365),
            "DAYS_EMPLOYED": -(years_employed * 365),
            "CODE_GENDER": gender,
            "NAME_CONTRACT_TYPE": contract_type,
            "NAME_EDUCATION_TYPE": education,
            "OCCUPATION_TYPE": occupation,
            "EXT_SOURCE_2": ext_source_2,
            "EXT_SOURCE_3": ext_source_3,
        }

        # ── SECTION 1 — RISK SCORE ──────────────────────────────
        st.markdown(
            '<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-size:1rem;'
            'font-weight:700;color:#e8eaf0;margin-bottom:1rem;">'
            '① Risk Score</p>',
            unsafe_allow_html=True
        )

        with st.spinner("Computing risk score..."):
            try:
                from src.ml.predict import predict_default
                result = predict_default(input_data)
                band = result["risk_band"]
                score = result["risk_score"]
                prob = result["probability"]

                color_map = {
                    "Low": "#22c87a",
                    "Medium": "#f5a623",
                    "High": "#f25c5c"
                }
                desc_map = {
                    "Low": "This applicant presents low credit risk. Historical patterns suggest a high probability of timely repayment.",
                    "Medium": "This applicant presents moderate credit risk. Manual review is recommended before approval.",
                    "High": "This applicant presents elevated credit risk. Approval should require additional documentation and collateral.",
                }
                color = color_map[band]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div style="background:#111318;border:1px solid #1f2330;
                                border-radius:12px;padding:1.75rem;text-align:center;
                                border-top:3px solid {color};">
                        <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;
                                    letter-spacing:0.1em;margin-bottom:0.5rem;">Risk Band</div>
                        <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                                    font-weight:800;color:{color};">{band}</div>
                        <div style="font-size:0.75rem;color:#6b7280;margin-top:4px;">
                            Classification</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background:#111318;border:1px solid #1f2330;
                                border-radius:12px;padding:1.75rem;text-align:center;
                                border-top:3px solid #4f8ef7;">
                        <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;
                                    letter-spacing:0.1em;margin-bottom:0.5rem;">Risk Score</div>
                        <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                                    font-weight:800;color:#4f8ef7;">
                            {score}<span style="font-size:1rem;color:#6b7280;">/100</span>
                        </div>
                        <div style="font-size:0.75rem;color:#6b7280;margin-top:4px;">
                            Composite Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div style="background:#111318;border:1px solid #1f2330;
                                border-radius:12px;padding:1.75rem;text-align:center;
                                border-top:3px solid #7c5cfc;">
                        <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;
                                    letter-spacing:0.1em;margin-bottom:0.5rem;">
                            Default Probability</div>
                        <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                                    font-weight:800;color:#7c5cfc;">{prob*100:.1f}%</div>
                        <div style="font-size:0.75rem;color:#6b7280;margin-top:4px;">
                            Model Confidence</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background:#111318;border:1px solid {color}33;
                            border-left:3px solid {color};border-radius:8px;
                            padding:1rem 1.25rem;margin-top:1rem;">
                    <div style="font-size:0.7rem;color:{color};text-transform:uppercase;
                                letter-spacing:0.1em;font-weight:600;margin-bottom:4px;">
                        Decision Guidance</div>
                    <div style="font-size:0.88rem;color:#9ca3af;">{desc_map[band]}</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Risk prediction error: {e}")
                return

        # ── SECTION 2 — SHAP EXPLANATION ───────────────────────
        st.markdown(
            '<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-size:1rem;'
            'font-weight:700;color:#e8eaf0;margin-bottom:0.25rem;">'
            '② Why this prediction? — SHAP Explanation</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-size:0.82rem;color:#6b7280;margin-bottom:1rem;">'
            'Top 10 features that drove this specific risk score. '
            'Red increases risk, green decreases risk.</p>',
            unsafe_allow_html=True
        )

        with st.spinner("Computing SHAP values..."):
            try:
                from src.ml.evaluate import explain_single_prediction
                from src.ml.predict import preprocess_single_input, load_model_artifacts

                model, encoders, feature_names = load_model_artifacts()
                explainer = shap.TreeExplainer(model)
                input_df = preprocess_single_input(
                    input_data, encoders, feature_names
                )
                explanation = explain_single_prediction(
                    model, explainer, input_df, index=0
                )

                fig, ax = plt.subplots(figsize=(10, 5))
                fig.patch.set_facecolor('#111318')
                ax.set_facecolor('#111318')
                colors = [
                    "#f25c5c" if v > 0 else "#22c87a"
                    for v in explanation["shap_value"]
                ]
                ax.barh(
                    explanation["feature"],
                    explanation["shap_value"],
                    color=colors,
                    height=0.6
                )
                ax.axvline(x=0, color="#1f2330", linewidth=1.5)
                ax.set_xlabel("SHAP Value", color="#6b7280", fontsize=9)
                ax.tick_params(colors="#9ca3af", labelsize=9)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_color("#1f2330")
                ax.spines["left"].set_color("#1f2330")
                ax.set_title(
                    "Feature Impact — Red increases risk · Green decreases risk",
                    color="#9ca3af", fontsize=10, pad=12
                )
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

                with st.expander("View detailed SHAP table"):
                    st.dataframe(
                        explanation[[
                            "feature", "feature_value",
                            "shap_value", "direction"
                        ]].reset_index(drop=True),
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"SHAP error: {e}")

        # ── SECTION 3 — DECISION RULES ──────────────────────────
        st.markdown(
            '<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-family:\'Syne\',sans-serif;font-size:1rem;'
            'font-weight:700;color:#e8eaf0;margin-bottom:0.25rem;">'
            '③ Decision Rules Triggered</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-size:0.82rem;color:#6b7280;margin-bottom:1rem;">'
            'Credit policy rules that fired for this applicant '
            'based on their input data.</p>',
            unsafe_allow_html=True
        )

        try:
            from src.ml.rules import evaluate_rules_for_applicant
            triggered = evaluate_rules_for_applicant(input_data)

            if not triggered:
                st.markdown("""
                <div style="background:#0f2d1e;border:1px solid #22c87a33;
                            border-left:3px solid #22c87a;border-radius:8px;
                            padding:1rem 1.25rem;">
                    <div style="font-size:0.88rem;color:#22c87a;font-weight:600;">
                        ✓ No rules triggered — applicant passes all policy checks.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="font-size:0.82rem;color:#6b7280;margin-bottom:0.75rem;">'
                    f'{len(triggered)} rule(s) triggered:</div>',
                    unsafe_allow_html=True
                )
                for rule in triggered:
                    color = rule["color"]
                    level = rule["risk_level"]
                    badge_bg = {
                        "High": "#2d1515",
                        "Medium": "#2d2010",
                        "Low": "#0f2d1e"
                    }[level]

                    st.markdown(f"""
                    <div style="background:#111318;border:1px solid {color}33;
                                border-left:3px solid {color};border-radius:8px;
                                padding:1.25rem 1.5rem;margin-bottom:0.75rem;">
                        <div style="display:flex;align-items:center;
                                    gap:0.75rem;margin-bottom:0.6rem;">
                            <span style="font-family:'JetBrains Mono',monospace;
                                         font-size:0.72rem;color:#6b7280;">
                                {rule["rule_id"]}</span>
                            <span style="font-family:'Syne',sans-serif;font-size:0.95rem;
                                         font-weight:700;color:#e8eaf0;">{rule["name"]}</span>
                            <span style="background:{badge_bg};color:{color};
                                         font-size:0.68rem;font-weight:600;
                                         padding:2px 10px;border-radius:20px;
                                         text-transform:uppercase;letter-spacing:0.08em;
                                         border:1px solid {color}33;margin-left:auto;">
                                {level} Risk</span>
                        </div>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                            <div>
                                <div style="font-size:0.68rem;color:#4f8ef7;
                                            text-transform:uppercase;letter-spacing:0.1em;
                                            margin-bottom:3px;">Rationale</div>
                                <div style="font-size:0.8rem;color:#9ca3af;line-height:1.5;">
                                    {rule["reason"]}</div>
                            </div>
                            <div>
                                <div style="font-size:0.68rem;color:#4f8ef7;
                                            text-transform:uppercase;letter-spacing:0.1em;
                                            margin-bottom:3px;">Recommended Action</div>
                                <div style="font-size:0.8rem;color:#9ca3af;line-height:1.5;">
                                    {rule["recommended_action"]}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Rules error: {e}")