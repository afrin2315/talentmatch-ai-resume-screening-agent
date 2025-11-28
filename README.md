TalentMatch – AI Resume Screening Agent
🔍 Overview

TalentMatch is an AI-powered ATS Resume Screening application that analyzes resumes against a Job Description (JD) and generates structured recruiter reports including:

ATS score (0–100)

Strengths

Weaknesses

Missing keywords

Hard/Soft skill match

Recruiter verdict (Strong/Medium/Weak Fit)

Professional ATS-style report card

This tool simplifies and speeds up the recruitment process by reducing manual resume screening.

🚀 Features

Upload multiple PDF resumes

Paste job description

Automatic PDF text extraction

AI-powered resume evaluation

Structured JSON-based scoring

ATS-style visual report with score ring

Ranking candidates by score

Beautiful full-width dark mode UI

Fast, accurate, and user-friendly

🧠 Tech Stack

Python

Streamlit

OpenAI GPT Models

pdfplumber

HTML + CSS + SVG

pandas (optional for future expansion)

📦 Installation
1. Clone the project
git clone <your-repository-link>
cd talentmatch-ai-resume-screening-agent

2. Create virtual environment
python -m venv venv
.\venv\Scripts\activate    # Windows

3. Install dependencies
pip install -r requirements.txt

4. Add API key

Create this file:

.streamlit/secrets.toml


Add your key:

[openai]
api_key = "YOUR_API_KEY"

▶️ Running the App

Run the Streamlit app:

streamlit run app.py


The app will open at:

http://localhost:8501

📁 Project Structure
├── app.py               → Main application
├── requirements.txt     → Dependencies
├── README.md            → Documentation
└── .streamlit/
     └── secrets.toml    → OpenAI API key

📌 Notes

Do NOT include your actual OpenAI key in public submissions.

Use sample resumes to test the system.

🏁 Conclusion

TalentMatch provides a modern, accurate, AI-powered resume analyzer that delivers recruiter-grade ATS reports efficiently. It improves shortlisting quality and reduces HR workload significantly.