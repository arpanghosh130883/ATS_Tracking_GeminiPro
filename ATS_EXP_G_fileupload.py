from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
import re

# Define the prompt template
prompt_template = """
Job Description: {job_description}
Resume: {resume_text}
JD Match: {jd_match}
Relevant Experience: {relevant_experience}

Please provide an analysis of the resume based on the job description with the following details:
- JD Match: {jd_match}%
- Relevant Experience: {relevant_experience} years
- Missing Keywords: [skills missing keywords],
- Overall Summary: [brief summary]
- Position Match: [Yes or No]
"""

def get_gemini_response(job_description, resume_text, jd_match, relevant_experience):
    # Format the input text using the prompt template
    input_text = prompt_template.format(job_description=job_description, resume_text=resume_text, jd_match=jd_match, relevant_experience=relevant_experience)
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

def calculate_relevant_experience(resume):
    experience_years = re.findall(r'(\d+) years? of experience', resume.lower())
    return max(experience_years) if experience_years else 0

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
        relevant_experience = calculate_relevant_experience(resume_text)
        response = get_gemini_response(job_description_text, resume_text, jd_match, relevant_experience)
        st.subheader("Analysis Result:")
        st.write(response)
    else:
        st.write("Please upload both the job description and the resume")
