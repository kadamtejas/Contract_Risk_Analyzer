import os
import fitz  # PyMuPDF
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import streamlit as st
import json

# ===============================
# Load Environment Variables
# ===============================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(page_title="📄 Contract Risk Analyzer", layout="wide")
st.title("📄 Contract Risk Analyzer App")

# ===============================
# File Uploader
# ===============================
uploaded_file = st.file_uploader("📂 Upload a Contract PDF", type=["pdf"])

if uploaded_file is not None:
    # Open PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"✅ Uploaded: {uploaded_file.name} | Pages: {len(doc)}")

    # Extract text from all pages
    text = ""
    for i, page in enumerate(doc, start=1):
        text += f"\n\n--- Page {i} ---\n\n{page.get_text('text')}"

    # ===============================
    # LLM Prompt
    # ===============================
    prompt = """
    You are an expert Contract Risk Analyzer. 

    Task:
    - Analyze the given contract text. 
    - Split it into individual clauses.
    - For each clause, extract the following details:
        - clause_id (numeric, incremental)
        - clause_heading (short descriptive title)
        - clause_text (short summary of the clause, max 2–3 sentences)
        - risk_level (High / Medium / Low)

    Contract text:
    {text}
    """

    prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
    final_prompt = prompt_template.format(text=text)

    # ===============================
    # Call Groq API
    # ===============================
    with st.spinner("🔍 Analyzing contract... Please wait"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="llama-3.3-70b-versatile"
        )
        result = chat_completion.choices[0].message.content

    # ===============================
    # Display Results
    # ===============================
    st.subheader("📑 Extracted Clauses & Risks")
    st.text_area("Raw LLM Output (JSON-like)", result, height=400)

    # Try to parse JSON if valid
    try:
        result_json = json.loads(result)
        df = pd.DataFrame(result_json["clauses"])
        st.subheader("📊 Structured Clauses")
        st.dataframe(df, use_container_width=True)
    except:
        st.warning("⚠️ Could not parse result into JSON. Please check formatting.")
