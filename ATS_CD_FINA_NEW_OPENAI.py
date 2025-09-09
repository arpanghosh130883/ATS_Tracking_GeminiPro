# app.py
# ------------------------------------------------------------
# pip install -U streamlit langchain langchain-openai python-dotenv scikit-learn PyPDF2
# streamlit run app.py
# ------------------------------------------------------------

from dotenv import load_dotenv
import streamlit as st
import os
import re
import PyPDF2 as pdf
from sklearn.feature_extraction.text import CountVectorizer

# use the modern OpenAI integration
from langchain_openai import ChatOpenAI

# -------------------- Setup --------------------
load_dotenv()  # loads OPENAI_API_KEY from .env if present

# Support Streamlit secrets too
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

if not OPENAI_KEY:
    st.warning(
        "OPENAI_API_KEY is not set. Add it to a .env file or Streamlit secrets.\n"
        "Example .env:\nOPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx"
    )

# Initialize LLM (chat)
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_KEY, temperature=0)

# -------------------- Prompt --------------------
PROMPT_TEMPLATE = """
Job Description: {job_description}
Resume: {resume_text}
JD Match: {jd_match}%

As an ATS scanner and a Technical HR Manager, please provide an analysis of the resume based on the job description with the following details:
- JD Match: {jd_match}%
- Experience: [years]
- Skills Missing: [skills missing keywords]
- Overall Summary: [brief summary]
- Position Match: {position_match}
"""

# -------------------- Helpers --------------------
def llm_analysis(job_description: str, resume_text: str, jd_match: float, position_match: str) -> str:
    """Call OpenAI chat model and return string content."""
    prompt = PROMPT_TEMPLATE.format(
        job_description=job_description,
        resume_text=resume_text,
        jd_match=jd_match,
        position_match=position_match,
    )
    resp = llm.invoke(prompt)  # returns an AIMessage
    return resp.content        # use .content (not .text)

def input_pdf_text(uploaded_file) -> str:
    reader = pdf.PdfReader(uploaded_file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_skills(text: str):
    return set(re.findall(r"\b\w+\b", text.lower()))

def calculate_jd_match(job_description: str, resume: str) -> float:
    jd_vectorizer = CountVectorizer(stop_words="english", ngram_range=(1, 2), max_features=50)
    _ = jd_vectorizer.fit_transform([job_description])
    jd_skills = set(jd_vectorizer.get_feature_names_out())

    resume_skills = extract_skills(resume)
    match_percentage = (len(jd_skills.intersection(resume_skills)) / len(jd_skills) * 100) if jd_skills else 0
    return round(match_percentage, 2)

def assess_position_match(jd_match: float, resume_text: str, job_description_text: str) -> str:
    jd_vectorizer1 = CountVectorizer(stop_words="english", ngram_range=(1, 2), max_features=50)
    _ = jd_vectorizer1.fit_transform([job_description_text])
    jd_skills = set(jd_vectorizer1.get_feature_names_out())

    resume_skills = extract_skills(resume_text)
    key_skills_present = jd_skills.issubset(resume_skills)
    return "<b style='color: black;'>Yes</b>" if (jd_match >= 38 or key_skills_present) else "<b style='color: black;'>No</b>"

# -------------------- UI --------------------
uploaded_job_description = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="job_description")
uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"], help="Please upload the resume in PDF format")

if uploaded_job_description is not None:
    st.success("Job Description PDF Uploaded Successfully")
if uploaded_resume is not None:
    st.success("Resume PDF Uploaded Successfully")

submit = st.button("Analyze Resume")

if submit:
    if not OPENAI_KEY:
        st.error("Missing OPENAI_API_KEY. Please set it in .env or Streamlit secrets.")
    elif uploaded_resume is not None and uploaded_job_description is not None:
        try:
            job_description_text = input_pdf_text(uploaded_job_description)
            resume_text = input_pdf_text(uploaded_resume)

            jd_match = calculate_jd_match(job_description_text, resume_text)
            position_match = assess_position_match(jd_match, resume_text, job_description_text)

            response_md = llm_analysis(job_description_text, resume_text, jd_match, position_match)

            st.subheader("Analysis Result:")
            st.metric("JD Match", f"{jd_match}%")
            st.markdown(f"**Position Match:** {position_match}", unsafe_allow_html=True)
            st.markdown(response_md, unsafe_allow_html=True)
        except Exception as e:
            st.exception(e)
    else:
        st.error("Please upload both the job description and the resume.")
