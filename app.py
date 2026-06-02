import streamlit as st

st.set_page_config(
    page_title="RiskLens AI — Credit Intelligence Platform",
    page_icon="assets/favicon.png" if __import__('os').path.exists("assets/favicon.png") else "🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --surface2:  #181b22;
    --border:    #1f2330;
    --accent:    #4f8ef7;
    --accent2:   #7c5cfc;
    --green:     #22c87a;
    --red:       #f25c5c;
    --amber:     #f5a623;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* Global resets */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Sidebar radio buttons */
[data-testid="stSidebar"] .stRadio label {
    font-family: var(--font-body) !important;
    font-size: 0.88rem !important;
    color: var(--muted) !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] .stRadio label:hover { color: var(--text) !important; background: var(--surface2) !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1.25rem 1.5rem !important;
}
[data-testid="stMetricLabel"] { font-family: var(--font-body) !important; color: var(--muted) !important; font-size: 0.78rem !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { font-family: var(--font-head) !important; color: var(--text) !important; font-size: 1.9rem !important; }

/* Forms and inputs */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
.stSelectbox select,
[data-baseweb="select"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}
[data-baseweb="select"] * { background: var(--surface2) !important; color: var(--text) !important; }

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

/* Form submit button */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    width: 100% !important;
    padding: 0.75rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}

/* Sliders */
[data-testid="stSlider"] .st-emotion-cache-1dp5vir { background: var(--accent) !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden !important; }

/* Code blocks */
.stCodeBlock, code { font-family: var(--font-mono) !important; background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }

/* Expander */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 0.75rem !important;
}
[data-testid="stChatInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

/* Info / warning / error boxes */
[data-testid="stAlert"] { border-radius: 8px !important; border-left-width: 3px !important; }

/* Spinner */
[data-testid="stSpinner"] * { color: var(--accent) !important; }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* Section headers */
h1, h2, h3, h4 { font-family: var(--font-head) !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }

/* Tab styling */
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    color: var(--muted) !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

/* JSON viewer */
[data-testid="stJson"] { background: var(--surface2) !important; border-radius: 8px !important; border: 1px solid var(--border) !important; }

/* Image captions */
[data-testid="stImage"] p { color: var(--muted) !important; font-size: 0.78rem !important; text-align: center !important; }

/* Plotly charts */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem 0;">
        <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#e8eaf0; letter-spacing:-0.02em; line-height:1.2;">
            RiskLens<span style="color:#4f8ef7;">AI</span>
        </div>
        <div style="font-size:0.72rem; color:#6b7280; letter-spacing:0.12em; text-transform:uppercase; margin-top:4px;">
            Credit Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1rem;"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Overview",
            "📊  EDA Dashboard",
            "🔮  Risk Assessment",
            "💬  Talk to Data",
            "📈  Model Metrics"
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div style="height:1px;background:#1f2330;margin:1rem 0;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem; color:#6b7280; line-height:1.7;">
        <div style="color:#4f8ef7; font-weight:600; margin-bottom:4px;">Model</div>
        LightGBM · 86 features<br>
        ROC-AUC: <span style="color:#22c87a;">0.7665</span><br><br>
        <div style="color:#4f8ef7; font-weight:600; margin-bottom:4px;">LLM</div>
        Groq · Llama 3.3 70B<br>
        NL → SQL chatbot<br><br>
        <div style="color:#4f8ef7; font-weight:600; margin-bottom:4px;">Pages</div>
        Overview · EDA · Risk Assessment<br>
        Talk to Data · Model Metrics
    </div>
    """, unsafe_allow_html=True)

# Route pages
if "Overview" in page:
    from ui.home import show; show()
elif "EDA" in page:
    from ui.eda_page import show; show()
elif "Risk Assessment" in page:
    from ui.prediction_page import show; show()
elif "Talk" in page:
    from ui.chatbot_page import show; show()
elif "Metrics" in page:
    from ui.metrics_page import show; show()