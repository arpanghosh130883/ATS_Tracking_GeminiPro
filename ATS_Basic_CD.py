from dotenv import load_dotenv

load_dotenv()
#import base64
import streamlit as st
import os
#import io
from PIL import Image 
#import pdf2image
import google.generativeai as genai
import PyPDF2 as pdf

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)",type=["pdf"],help="Please uplaod the pdf")


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume for Data Engineering Role")

submit2 = st.button("Tell Me About the Resume for Java/.Net developer Role")

submit3 = st.button("Tell Me About the Resume for Sales Person Role")

submit4 = st.button("Tell Me About the Resume for Marketing Role")

submit5 = st.button("Tell Me About the Resume for Technical QA Role")

#Input prompt for the first submit button
input_prompt1 = """

{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "As an ATS scanner and a Technical HR Manager with expertise in the tech field, including software engineering and data-related roles, my task is to review the provided resume against the job description for a Senior Data Engineer position. In this review, I will assess the candidate's qualifications, technical skills, and experience in data engineering, focusing on areas crucial for this role such as advanced data processing, big data technologies, cloud computing platforms (e.g., AWS, Azure, GCP), ETL processes, database management, and programming skills, particularly in Python and SQL. I will also consider their experience with data warehousing, data modeling, and data pipeline development. Based on these criteria, I will highlight the strengths and weaknesses of the applicant, noting how well their profile aligns with the job requirements. The percentage match will reflect the degree to which the candidate meets the specific technical and experiential demands of a Senior Data Engineer role, and I will identify any significant missing keywords or skill gaps relevant to this position. 

}


"""

#Input prompt for the third submit button
input_prompt2 = """

{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "As an ATS scanner and Technical HR Manager with specialized knowledge in the tech field, particularly in Java and .Net development, my task is to review the provided resume against the job description for a Java/.Net Developer position. In this evaluation, I will scrutinize the candidate's proficiency in Java and .Net frameworks, their experience with object-oriented programming, familiarity with front-end technologies (like JavaScript, HTML, CSS), and back-end development skills (including database management with SQL). I will also assess their knowledge of software development best practices, such as version control with Git and Agile methodologies. The percentage match will be assigned based on how closely the candidate's skills and experiences align with the requirements of a Java/.Net Developer role. I will identify the strengths of the applicant, such as strong Java/.Net coding skills or experience in full-stack development, and point out any weaknesses or missing key skills pertinent to the job description."

  }


"""

#Input prompt for the fourth submit button
input_prompt3 = """

{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "As an ATS scanner and Technical HR Manager with a profound understanding of the Sales field, especially in fintech and currency exchange domains, my task is to review the provided resume against the job description for a Senior Sales position at a company like Currencies Direct Solution Pvt Ltd. This evaluation will focus on the candidate's expertise in financial products, particularly in foreign exchange, their experience in sales within the fintech sector, and their ability to manage and grow client portfolios. Key competencies such as knowledge of financial markets, customer relationship management, negotiation skills, and proficiency in fintech tools will be assessed. The percentage match will reflect how well the candidate's background and skills align with the specific demands of a Senior Sales role in currency exchange. Strengths, such as a proven sales track record in the fintech industry or exceptional client management skills, will be highlighted, along with any weaknesses or missing key competencies essential for success in this role."

  }

"""

#Input prompt for the fourth submit button
input_prompt4 = """

{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "As an ATS scanner and Technical HR Manager with extensive knowledge of the Marketing field, particularly in the fintech and foreign exchange domain, my task is to review the provided resume against the job description for a Senior Marketing position at a company like Currencies Direct Solution Pvt Ltd. This evaluation will concentrate on the candidate's experience in marketing financial services, their proficiency in digital marketing strategies tailored to the fintech sector, and their understanding of global currency markets. Essential skills such as campaign management, data-driven marketing analysis, expertise in SEO/SEM, content creation, and CRM systems will be assessed. The percentage match will be calculated based on how well the candidate's profile aligns with the key requirements of a Senior Marketing role in the currency exchange industry. Strengths, such as a successful track record in digital marketing within fintech or exceptional market analysis capabilities, will be underscored, along with any weaknesses or absence of critical skills vital for this specialized marketing role."
  
  }

"""

#Input prompt for the fourth submit button
input_prompt5 = """

{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "As an ATS scanner and Technical HR Manager with extensive knowledge in the tech field, focusing on software engineering and quality assurance, my task is to review the provided resume against the job description for a Test Engineer and Technical QA role. This assessment will concentrate on the candidate's experience and skills in software testing, data validation, Python scripting for automated tests, as well as their familiarity with QA methodologies and tools. I will evaluate the candidate's proficiency in test planning, execution, defect tracking, and their ability to work with complex data systems. The percentage match will be calculated based on how well the candidate's qualifications align with the requirements for a Test Engineer and Technical QA, particularly in software and data engineering environments. Strengths such as a strong background in Python for automation, experience with various testing frameworks, and a solid understanding of the software development lifecycle will be highlighted. Any weaknesses or missing essential skills, like specific QA tools or testing methodologies, will also be identified."
  
  }

"""

if submit1:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt1)
        st.subheader(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt2)
        st.subheader(response)

elif submit3:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt3)
        st.subheader(response)

elif submit4:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt4)
        st.subheader(response)

elif submit5:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt5)
        st.subheader(response)
    else:
        st.write("Please uplaod the resume")