import streamlit as st

EXAMPLE_QUESTIONS = [
    "What is the overall default rate?",
    "Which gender has a higher default rate?",
    "Average income of defaulters vs non-defaulters?",
    "Top 5 occupations with highest default rate?",
    "How many applicants have more than 3 previous loans?",
    "What is the average credit amount by contract type?",
]

def show():
    st.markdown("""
    <div style="padding:1.5rem 0 1rem 0;">
        <div style="font-size:0.72rem;color:#f5a623;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Module 05</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#e8eaf0;letter-spacing:-0.02em;margin:0 0 0.5rem 0;">Talk to Data</h1>
        <p style="color:#6b7280;font-size:0.9rem;margin:0;">Ask questions in plain English. Groq/Llama 3.3 converts them to SQL and returns business insights.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2330;margin-bottom:1.5rem;"></div>', unsafe_allow_html=True)

    # Example questions
    st.markdown('<p style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;">Quick Questions</p>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 3]:
            if st.button(q, key=f"ex_{i}", use_container_width=True):
                st.session_state.pending_question = q

    st.markdown('<div style="height:1px;background:#1f2330;margin:1.25rem 0;"></div>', unsafe_allow_html=True)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sql" in msg:
                with st.expander("View generated SQL"):
                    st.code(msg["sql"], language="sql")
            if "dataframe" in msg and not msg["dataframe"].empty:
                with st.expander("View raw query results"):
                    st.dataframe(msg["dataframe"], use_container_width=True)

    # Handle example click
    if "pending_question" in st.session_state:
        question = st.session_state.pop("pending_question")
        st.session_state.messages.append({"role": "user", "content": question})
        _process(question)
        st.rerun()

    # Text input
    if question := st.chat_input("Ask anything about the credit data..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        _process(question)
        st.rerun()


def _process(question: str):
    with st.spinner("Querying data..."):
        try:
            from src.talk_to_data.query_runner import ask_question
            result = ask_question(question)
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sql": result["sql"],
                "dataframe": result["results"]
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {str(e)}"
            })