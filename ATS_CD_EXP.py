from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
import json  # Import JSON to parse the response

def get_gemini_response(job_description, resume_text):
    input_text = {
        "Job Description": job_description,
        "Resume": resume_text
    }
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(json.dumps(input_text))  # Convert input to JSON string
    try:
        return json.loads(response.text)  # Parse the response as JSON
    except json.JSONDecodeError:
        return {"error": "Invalid response from model"}

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
        if "error" in response:
            st.write(response["error"])
        else:
            st.write(f"JD Match: {response.get('JD Match', 'N/A')}%")
            st.write(f"Relevant Experience: {response.get('Relevant Experience', 'N/A')}%")
            st.write(f"Missing Keywords: {', '.join(response.get('Missing Keywords', []))}")
            st.write(f"Profile Summary: {response.get('Profile Summary', 'N/A')}")
    else:
        st.write("Please upload the resume and provide the job description")
