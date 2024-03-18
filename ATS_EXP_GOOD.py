from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os

def get_gemini_response(job_description, resume_text):
    input_text = f"Job Description: {job_description}\nResume: {resume_text}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
job_description = st.text_area("Job Description:", key="job_description")
uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"], help="Please upload the resume in PDF format")

if uploaded_resume is not None:
    st.write("PDF Uploaded Successfully")

submit = st.button("Analyze Resume")

if submit:
    if uploaded_resume is not None and job_description:
        resume_text = input_pdf_text(uploaded_resume)
        response = get_gemini_response(job_description, resume_text)
        st.subheader("Analysis Result:")
        st.write(response)
    else:
        st.write("Please upload the resume and provide the job description")
