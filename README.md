TalentMatch – AI Resume Screening Agent
🌟 Introduction

TalentMatch is a simple and effective AI tool that helps compare resumes with a given job description. Instead of manually checking every resume, the app uses AI to extract text, understand skills, and generate a clean ATS-style report. The goal is to save time for recruiters and give a fair, structured evaluation of each candidate.

🚀 What the App Can Do

Accepts multiple PDF resumes at once

Extracts text automatically from each resume

Lets you paste any Job Description (JD)

Uses AI to evaluate resumes based on the JD

Generates:

Overall ATS Score

Strengths

Weaknesses

Missing keywords

Hard & soft skill match

Final verdict (Strong / Medium / Weak Fit)

Displays everything inside a clean, dark-themed dashboard

Ranks all candidates from highest to lowest score

The app is designed to be simple enough for beginners and reliable enough for real use.

🧠 Technology Used

This project is built using:

Python

Streamlit for the UI

OpenAI models for the evaluation

pdfplumber for reading PDF resumes

HTML + CSS + SVG for the custom ATS report design

pandas for handling structured data (optional)

📦 How to Install and Run
1. Clone the repository
git clone https://github.com/afrin2315/talentmatch-ai-resume-screening-agent
cd talentmatch-ai-resume-screening-agent

2. Create a virtual environment
python -m venv venv
.\venv\Scripts\activate    # Windows

3. Install required packages
pip install -r requirements.txt

4. Add your OpenAI API key

Create this file:

.streamlit/secrets.toml


Add your key like this:

[openai]
api_key = "YOUR_API_KEY"
(Do NOT upload your real API key to GitHub.)

5. Start the application
streamlit run app.py


Your browser will open automatically at:

[http://localhost:8501](http://localhost:8501/)

📁 Project Layout
├── app.py                      → Main application
├── requirements.txt            → Dependencies
├── README.md                   → Documentation
├── sample/
│     ├── sample_resume.pdf     → Dummy resume for testing
│     └── sample_jd.pdf         → Dummy JD for testing
└── .streamlit/
      └── secrets.toml          → API key (not included in public repo)

📝 About the Sample Files

The “sample” folder has two dummy files that help anyone quickly test the app:
sample_resume.pdf – A basic Data Analyst–style resume
sample_jd.pdf – A simple JD with expected skills
These are intentionally simple and contain no personal data.

🔒 Important Notes

Never expose your actual API key in public repositories
Only upload dummy resumes when demonstrating
The app is meant for educational and prototype purposes

🎯 Final Thoughts

TalentMatch makes resume evaluation faster, cleaner, and more structured.
It was created with the intention of solving a real problem in recruitment—
reducing time spent on manual screening and giving consistent, AI-based insights.

The project is lightweight, easy to run, and ready for further improvements or integration.
