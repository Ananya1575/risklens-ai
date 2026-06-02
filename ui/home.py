import streamlit as st

def show():
    st.markdown("""
    <div style="padding: 2.5rem 0 1rem 0;">
        <div style="font-size:0.75rem;color:#4f8ef7;letter-spacing:0.15em;text-transform:uppercase;font-family:'DM Sans',sans-serif;margin-bottom:0.75rem;">
            Home Credit Default Risk · 307,511 Applicants
        </div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.03em;line-height:1.1;margin:0 0 1rem 0;">
            AI-Powered Credit<br>Risk Intelligence
        </h1>
        <p style="font-size:1rem;color:#9ca3af;max-width:560px;line-height:1.7;margin:0;">
            End-to-end machine learning platform for loan default prediction, 
            explainability, and natural language data exploration.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin:1.5rem 0;"></div>', unsafe_allow_html=True)

    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        ("307,511", "Total applicants"),
        ("8.07%", "Default rate"),
        ("0.7665", "ROC-AUC score"),
        ("86", "Model features"),
        ("11.39×", "Class imbalance"),
    ]
    for col, (val, label) in zip([col1,col2,col3,col4,col5], kpis):
        with col:
            st.markdown(f"""
            <div style="background:#111318;border:1px solid #1f2330;border-radius:10px;padding:1.2rem 1rem;">
                <div style="font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:800;color:#e8eaf0;">{val}</div>
                <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # Feature cards
    st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;color:#e8eaf0;margin-bottom:1rem;">Platform Modules</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        (col1, "📊", "EDA Dashboard", "6 interactive charts exploring demographics, income, credit ratios, and missing data patterns across 307K applicants.", "#4f8ef7"),
        (col2, "🔮", "Risk Assessment", "Enter applicant data once — get risk score, SHAP explanation, and triggered decision rules all in one unified view.", "#7c5cfc"),
        (col3, "💬", "Talk to Data", "Ask questions in plain English. Groq/Llama 3.3 converts them to SQL and returns instant business insights.", "#f5a623"),
    ]
    for col, icon, title, desc, color in cards:
        with col:
            st.markdown(f"""
            <div style="background:#111318;border:1px solid #1f2330;border-radius:12px;padding:1.5rem;height:160px;border-top:3px solid {color};">
                <div style="font-size:1.5rem;margin-bottom:0.6rem;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#e8eaf0;margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.8rem;color:#6b7280;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards2 = [
        (col1, "📈", "Model Metrics", "ROC-AUC, confusion matrix, precision-recall, and feature importance — full LightGBM evaluation on 61,503 test samples.", "#f25c5c"),
        (col2, "🐳", "Docker Ready", "Fully containerized with Dockerfile and docker-compose. Deploy the entire platform with a single command.", "#4f8ef7"),
        (col3, "📋", "Decision Rules", "10 business-readable credit policy rules derived from ML insights — included inside the Risk Assessment page.", "#22c87a"),
    ]
    for col, icon, title, desc, color in cards2:
        with col:
            st.markdown(f"""
            <div style="background:#111318;border:1px solid #1f2330;border-radius:12px;padding:1.5rem;height:160px;border-top:3px solid {color};">
                <div style="font-size:1.5rem;margin-bottom:0.6rem;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#e8eaf0;margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.8rem;color:#6b7280;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    # Key findings
    st.markdown('<p style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;color:#e8eaf0;margin-bottom:1rem;">Key Findings from EDA</p>', unsafe_allow_html=True)

    findings = [
        ("#f25c5c", "8.07%", "overall default rate", "Heavily imbalanced dataset — handled with scale_pos_weight in LightGBM."),
        ("#f5a623", "12.3%", "default rate age 20-25", "Youngest applicants default at 2.5× the rate of those over 60."),
        ("#f25c5c", "17.15%", "low-skill laborer default", "Highest-risk occupation — nearly double the overall average."),
        ("#4f8ef7", "10.1%", "male default rate", "Male applicants default at 44% higher rate than female applicants (7.0%)."),
        ("#22c87a", "Top Signal", "EXT_SOURCE features", "External credit bureau scores (EXT_SOURCE_2, EXT_SOURCE_3) are the strongest predictors of default risk."),   
    ]

    for color, val, label, desc in findings:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:1rem;background:#111318;border:1px solid #1f2330;border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.5rem;">
            <div style="min-width:70px;font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:{color};">{val}</div>
            <div>
                <div style="font-size:0.82rem;font-weight:600;color:#e8eaf0;text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
                <div style="font-size:0.8rem;color:#6b7280;margin-top:2px;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)