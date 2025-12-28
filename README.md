🔍 AI-Powered Applicant Tracking System (ATS)


📌 Overview

This project implements an AI-driven Applicant Tracking System (ATS) using OpenAI Large Language Models.
The system evaluates resumes against job descriptions to provide structured candidate fit analysis, enabling recruiters to make faster, data-driven shortlisting decisions.

🎯 Objectives

Automate resume screening

Improve hiring accuracy and consistency

Reduce recruiter manual effort

Provide explainable hiring insights

✨ Key Features

Resume parsing (PDF/DOCX)

Job description understanding

AI-based skill & experience matching

Candidate scoring and ranking

Skill gap analysis

ATS-friendly structured outputs

🧠 High-Level Architecture
Resume + Job Description
        ↓
Text Extraction
        ↓
Prompt Engineering
        ↓
OpenAI LLM
        ↓
Structured Evaluation (JSON)
        ↓
UI / API Output

🛠 Tech Stack

Python

OpenAI GPT-4 / GPT-4o

LangChain

FastAPI / Streamlit

PyPDF / pdfplumber

📂 Folder Structure
ats-openai/
├── app.py
├── resume_parser.py
├── ats_engine.py
├── prompts/
├── requirements.txt
└── README.md

🧪 Sample Output
{
  "overall_fit": "Strong",
  "skill_match_percentage": 82,
  "experience_match": "Relevant",
  "missing_skills": ["Kubernetes"],
  "recommendation": "Shortlist"
}

🚀 Use Cases

Campus hiring

Lateral recruitment

Consulting staffing

Internal mobility
