import streamlit as st
from src.ml.rules import get_all_rules, get_rules_summary, evaluate_rules_for_applicant


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#7c5cfc;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Module 04B</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">Decision Rules</h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">Business-readable credit policy rules derived from ML insights and EDA findings.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    # Summary stats
    summary = get_rules_summary()
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        (col1, summary["total"], "Total Rules", "#4f8ef7"),
        (col2, summary["high"], "High Risk Rules", "#f25c5c"),
        (col3, summary["medium"], "Medium Risk Rules", "#f5a623"),
        (col4, summary["low"], "Low Risk Rules", "#22c87a"),
    ]
    for col, val, label, color in stats:
        with col:
            st.markdown(f"""
            <div style="background:#111318;border:1px solid #1f2330;border-radius:10px;
                        padding:1.25rem;text-align:center;border-top:3px solid {color};">
                <div style="font-family:'Syne',sans-serif;font-size:2rem;
                            font-weight:800;color:{color};">{val}</div>
                <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;
                            letter-spacing:0.08em;margin-top:4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Filter
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;color:#e8eaf0;margin-bottom:1rem;">All Credit Policy Rules</p>', unsafe_allow_html=True)
    with col2:
        filter_level = st.selectbox(
            "Filter by risk",
            ["All", "High", "Medium", "Low"],
            label_visibility="collapsed"
        )

    rules = get_all_rules()
    if filter_level != "All":
        rules = [r for r in rules if r["risk_level"] == filter_level]

    for rule in rules:
        color = rule["color"]
        level = rule["risk_level"]
        badge_bg = {"High": "#2d1515", "Medium": "#2d2010", "Low": "#0f2d1e"}[level]

        st.markdown(f"""
        <div style="background:#111318;border:1px solid #1f2330;border-left:3px solid {color};
                    border-radius:8px;padding:1.25rem 1.5rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                             color:#6b7280;">{rule["rule_id"]}</span>
                <span style="font-family:'Syne',sans-serif;font-size:0.95rem;
                             font-weight:700;color:#e8eaf0;">{rule["name"]}</span>
                <span style="background:{badge_bg};color:{color};font-size:0.68rem;
                             font-weight:600;padding:2px 10px;border-radius:20px;
                             text-transform:uppercase;letter-spacing:0.08em;
                             border:1px solid {color}33;margin-left:auto;">
                    {level} Risk
                </span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-top:0.5rem;">
                <div>
                    <div style="font-size:0.68rem;color:#4f8ef7;text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:3px;">Condition</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;
                                color:#9ca3af;">{rule["condition"]}</div>
                </div>
                <div>
                    <div style="font-size:0.68rem;color:#4f8ef7;text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:3px;">Rationale</div>
                    <div style="font-size:0.8rem;color:#9ca3af;line-height:1.5;">
                        {rule["reason"]}</div>
                </div>
                <div>
                    <div style="font-size:0.68rem;color:#4f8ef7;text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:3px;">Action</div>
                    <div style="font-size:0.8rem;color:#9ca3af;line-height:1.5;">
                        {rule["recommended_action"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>', unsafe_allow_html=True)

    # Rule evaluator
    st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;color:#e8eaf0;margin-bottom:0.25rem;">Rule Evaluator</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#6b7280;margin-bottom:1rem;">Enter applicant details to see which rules are triggered.</p>', unsafe_allow_html=True)

    with st.form("rules_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input("Annual Income", value=150000, step=5000)
            credit = st.number_input("Loan Amount", value=500000, step=10000)
        with col2:
            age = st.slider("Age (Years)", 18, 70, 35)
            years_emp = st.slider("Years Employed", 0, 40, 3)
        with col3:
            ext2 = st.slider("Ext Credit Score 2", 0.0, 1.0, 0.5, 0.01)
            ext3 = st.slider("Ext Credit Score 3", 0.0, 1.0, 0.5, 0.01)
            contract = st.selectbox("Contract Type", ["Cash loans", "Revolving loans"])

        submitted = st.form_submit_button("→  Evaluate Rules", use_container_width=True)

    if submitted:
        input_dict = {
            "DAYS_BIRTH": -(age * 365),
            "EXT_SOURCE_2": ext2,
            "EXT_SOURCE_3": ext3,
            "AMT_INCOME_TOTAL": income,
            "AMT_CREDIT": credit,
            "DAYS_EMPLOYED": -(years_emp * 365),
            "NAME_CONTRACT_TYPE": contract,
        }

        triggered = evaluate_rules_for_applicant(input_dict)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        if not triggered:
            st.markdown("""
            <div style="background:#0f2d1e;border:1px solid #22c87a33;border-left:3px solid #22c87a;
                        border-radius:8px;padding:1rem 1.25rem;">
                <div style="font-size:0.88rem;color:#22c87a;font-weight:600;">
                    ✓ No rules triggered — applicant passes all policy checks.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-size:0.82rem;color:#6b7280;margin-bottom:0.75rem;">
                {len(triggered)} rule(s) triggered for this applicant:
            </div>
            """, unsafe_allow_html=True)

            for rule in triggered:
                color = rule["color"]
                st.markdown(f"""
                <div style="background:#111318;border:1px solid {color}33;
                            border-left:3px solid {color};border-radius:8px;
                            padding:1rem 1.25rem;margin-bottom:0.5rem;">
                    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:4px;">
                        <span style="font-family:'JetBrains Mono',monospace;
                                     font-size:0.7rem;color:#6b7280;">{rule["rule_id"]}</span>
                        <span style="font-size:0.88rem;font-weight:600;color:{color};">
                            {rule["name"]}</span>
                    </div>
                    <div style="font-size:0.8rem;color:#9ca3af;">{rule["recommended_action"]}</div>
                </div>
                """, unsafe_allow_html=True)