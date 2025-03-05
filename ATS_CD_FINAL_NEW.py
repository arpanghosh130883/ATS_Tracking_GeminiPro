from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import re
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt template
prompt_template = """
Job Description: {job_description}
Resume: {resume_text}
JD Match: {jd_match}

Please provide an analysis of the resume based on the job description with the following details:
- JD Match: {jd_match}%
- Experience: [years]
- Skills Missing: [skills missing keywords],
- Overall Summary: [brief summary]
- Position Match: {position_match}
"""

def get_gemini_response(job_description, resume_text, jd_match, position_match):
    # Format the input text using the prompt template
    input_text = prompt_template.format(job_description=job_description, resume_text=resume_text, jd_match=jd_match, position_match=position_match)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def calculate_jd_match(job_description, resume):
    jd_skills = set(re.findall(r'\b\w+\b', job_description.lower()))
    resume_skills = set(re.findall(r'\b\w+\b', resume.lower()))
    match_percentage = len(jd_skills.intersection(resume_skills)) / len(jd_skills) * 100 if jd_skills else 0
    return round(match_percentage, 2)

def extract_skills(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def assess_position_match(jd_match, resume_text, job_description_text):
    #relevant_experience = 3  # Placeholder, replace with actual calculation
    jd_skills = extract_skills(job_description_text)
    resume_skills = extract_skills(resume_text)
    key_skills_present = jd_skills.issubset(resume_skills)
    if jd_match >= 50 or key_skills_present: #relevant_experience >= 3:
        return "Yes"
    else:
        return "No"

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
uploaded_job_description = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="job_description")
uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"], help="Please upload the resume in PDF format")

if uploaded_job_description is not None:
    st.write("Job Description PDF Uploaded Successfully")

if uploaded_resume is not None:
    st.write("Resume PDF Uploaded Successfully")

submit = st.button("Analyze Resume")

if submit:
    if uploaded_resume is not None and uploaded_job_description is not None:
        job_description_text = input_pdf_text(uploaded_job_description)
        resume_text = input_pdf_text(uploaded_resume)
        jd_match = calculate_jd_match(job_description_text, resume_text)
        position_match = assess_position_match(jd_match, resume_text, job_description_text)
        response = get_gemini_response(job_description_text, resume_text, jd_match, position_match)
        st.subheader("Analysis Result:")
        st.write(response)
    else:
        st.write("Please upload both the job description and the resume")
