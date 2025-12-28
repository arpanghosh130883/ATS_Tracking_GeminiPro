ATS Application using OpenAI
AI-Powered Applicant Tracking System (ATS)


📌 Project Overview

This project implements an AI-driven Applicant Tracking System (ATS) that leverages OpenAI LLMs to automate resume screening, candidate scoring, and job-fit analysis. The system evaluates resumes against job descriptions and produces structured, explainable hiring insights.

The goal is to reduce recruiter effort, improve shortlisting accuracy, and ensure bias-aware, consistent screening.

🎯 Key Features

Resume parsing (PDF/DOCX)

Job Description understanding

AI-based candidate scoring

Skills gap analysis

Experience relevance scoring

ATS-friendly feedback generation

Explainable AI outputs for recruiters

🧠 Architecture
Resume (PDF/DOCX)
        ↓
Text Extraction (PDF Parser)
        ↓
Prompt Engineering
        ↓
OpenAI LLM
        ↓
Structured Evaluation (JSON)
        ↓
UI / API Output

🛠️ Tech Stack

Python

OpenAI GPT-4 / GPT-4o

LangChain

FastAPI / Streamlit

PyPDF / pdfplumber

Pydantic

Docker (optional)

📂 Project Structure
ats-openai/
├── app.py
├── prompts/
│   ├── resume_eval.txt
│   └── skill_gap.txt
├── parsers/
│   └── resume_parser.py
├── services/
│   └── ats_engine.py
├── requirements.txt
└── README.md

⚙️ How It Works

Upload resume + JD

Resume is parsed into structured text

LLM evaluates:

Skill match %

Experience relevance

Red flags

Final hire recommendation

Output returned in JSON + human-readable format








**ATS Resume Expert**

**Overview**
ATS Resume Expert is a Streamlit application designed to assist job seekers in optimizing their resumes for Applicant Tracking Systems (ATS) and specific job roles. The application leverages the power of the Gemini model from Google's Generative AI to analyze resumes and provide insights into their alignment with job descriptions.

**Features**

**Job Description Analysis**:  Users can input a job description to set the context for resume evaluation.

**Resume Upload:** The application allows users to upload their resumes in PDF format for analysis.

**Role-Specific Feedback:** Users can select from various job roles (e.g., Data Engineering, Java/.Net Developer, Salesperson, Marketing, Technical QA) to receive tailored feedback on their resumes.

**Resume Insights:**  The application provides a percentage match with the job description, highlights missing keywords, and offers a profile summary with suggestions for improvement.


**Installation**
To run the ATS Resume Expert application locally, follow these steps:

**Clone the repository:**

git clone https://github.com/your-username/ats-resume-expert.git

**Navigate to the project directory:**

cd ats-resume-expert


**Install the required dependencies:**
pip install -r requirements.txt


**Run the Streamlit application:** 

streamlit run app.py


**Usage**

1. Open the application in your web browser.
2. Enter a job description in the provided text area.
3. Upload your resume in PDF format.
4. Select the job role you are interested in.
5. Click the corresponding button to receive feedback on your resume.
6. Review the insights and suggestions to improve your resume's alignment with the job description.

**Technologies Used** 

Streamlit
Google Generative AI (Gemini model)
PyPDF2
Python

**Acknowledgments**

Thanks to Google Generative AI for providing the Gemini model for content generation.
Special thanks to the Streamlit community for their support and resources.
