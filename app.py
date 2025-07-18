import streamlit as st
import pandas as pd
from llm import explain_error, extract_summary, categorize_newman

st.set_page_config(page_title="Student Error Explainer", layout="wide")
st.title("📘 AI-Powered Student Mistake Analyzer")

# --- App Overview ---
with st.expander("🔍 What this App Does", expanded=True):
    st.markdown("""
    This tool uses advanced AI (GPT-4o or Gemini Pro) to analyze students’ math responses by:

    - 🔎 Comparing each student’s answer with the correct answer.
    - 📄 Explaining the mathematical mistake or misunderstanding.
    - 🏷 Categorizing the error into types like:
        - Omission Error, Incorrect Value, Conceptual Misunderstanding, etc.
    - 🧠 Classifying the mistake using **Newman’s Error Analysis** (NEA):
        - Reading, Comprehension, Transformation, Process Skill, Encoding

    This helps educators quickly identify where students struggle and provide targeted support.
    """)

# --- Sidebar: LLM Configuration ---
st.sidebar.header("🧠 LLM Settings")
llm_choice = st.sidebar.selectbox("Choose LLM Provider", ["OpenAI GPT-4o", "Gemini Pro"])

if llm_choice == "OpenAI GPT-4o":
    openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
    gemini_api_key = None
else:
    gemini_api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")
    openai_api_key = None

if not openai_api_key and not gemini_api_key:
    st.warning("⚠️ Please enter at least one valid API key to proceed.")

# --- Sidebar: Instruction Context ---
st.sidebar.header("📝 Math Concept Instruction Inbox")
instruction_note = st.sidebar.text_area(
    "Add optional math concept info for the LLM (e.g. formulas, notation tips):",
    placeholder="""Examples:
- cc(a,b) = [a,b], co(a,b) = [a,b)
- 'ansa' is usually a value (e.g. radius); 'ansb' is for sketching
- Division by zero is undefined
- sin²x + cos²x = 1 is an identity
""",
    height=220
)

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload CSV (columns: student_id, response, right_answer)", type="csv")

if uploaded_file and (openai_api_key or gemini_api_key):
    df = pd.read_csv(uploaded_file)

    if not {'student_id', 'response', 'right_answer'}.issubset(df.columns):
        st.error("❌ CSV must contain: student_id, response, right_answer")
        st.stop()

    st.write("✅ Preview of Uploaded Data:")
    st.dataframe(df.head(), use_container_width=True)

    if st.button("🚀 Analyze Mistakes"):
        llm_responses, error_summaries, error_categories = [], [], []

        progress = st.progress(0)
        with st.spinner("🔎 Analyzing responses with LLM..."):
            for i, row in enumerate(df.itertuples(), 1):
                explanation = explain_error(
                    row.response, row.right_answer,
                    openai_api_key, gemini_api_key,
                    instruction_note, llm_choice
                )
                summary = extract_summary(explanation, openai_api_key, gemini_api_key, llm_choice)
                category = categorize_newman(explanation, openai_api_key, gemini_api_key, llm_choice)

                llm_responses.append(explanation)
                error_summaries.append(summary)
                error_categories.append(category)
                progress.progress(i / len(df))

        df["llm_response"] = llm_responses
        df["error_summary"] = error_summaries
        df["error_category"] = error_categories

        st.success("✅ Analysis complete!")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, file_name="student_errors_analyzed.csv", mime="text/csv")
        st.success("🎉 Done! You can now download the results.")
