import os
import json
import pdfplumber
import html as html_escape
import streamlit as st
from streamlit.components.v1 import html as st_html
from openai import OpenAI


# =========================================================
# OPENAI CLIENT
# =========================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or (
    st.secrets.get("openai", {}).get("api_key") if "openai" in st.secrets else None
)

if not OPENAI_API_KEY:
    st.warning("⚠️ OPENAI_API_KEY missing. Please configure it.")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="TalentMatch – AI Resume Screening Agent",
    layout="wide",
    page_icon="📊"
)


# =========================================================
# GLOBAL APP CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #1a0047 50%, #33009c 100%) !important;
}

/* Full width */
.block-container {
    max-width: 100% !important;
}

/* Inputs */
textarea, input[type=text] {
    background:#000 !important;
    color:#fff !important;
    border:1px solid #8a65ff !important;
    border-radius:12px !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg,#4a00dd,#9d4dff) !important;
    color:white !important;
    border-radius:12px !important;
    padding:12px 24px !important;
    font-size:18px !important;
    font-weight:700 !important;
}
</style>
""", unsafe_allow_html=True)



# =========================================================
# PDF TEXT EXTRACTION
# =========================================================
def extract_text(pdf):
    try:
        with pdfplumber.open(pdf) as p:
            return "\n".join([(page.extract_text() or "") for page in p.pages])
    except:
        return ""


# =========================================================
# SAFE JSON PARSER
# =========================================================
def safe_json(text):
    try:
        return json.loads(text)
    except:
        pass
    s = text.find("{")
    e = text.rfind("}")
    if s != -1 and e != -1:
        try:
            return json.loads(text[s:e+1])
        except:
            return None
    return None


# =========================================================
# CALL OPENAI
# =========================================================
def call_ai(jd, resume):
    if client is None:
        return None

    schema = """
{
  "score":0-100,
  "reason":"text",
  "job_match":"Strong/Medium/Weak",
  "strengths":[],
  "weaknesses":[],
  "hard_skill_match":0-100,
  "soft_skill_match":0-100,
  "missing_keywords":[],
  "recommendations":[],
  "recommended_courses":[],
  "resume_improvements":[],
  "verdict":"Strong Fit/Medium Fit/Weak Fit"
}
"""

    prompt = f"""
Return ONLY valid JSON.

Job Description:
{jd}

Resume:
{resume}

JSON Schema (required):
{schema}
"""

    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an ATS scoring engine. Output ONLY JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )
        return safe_json(r.choices[0].message.content)
    except:
        return None


# =========================================================
# CARD HTML (WITH INTERNAL CSS)
# =========================================================
def card(name, info):

    score = int(info.get("score", 0))
    hard = int(info.get("hard_skill_match", 0))
    soft = int(info.get("soft_skill_match", 0))

    # SVG circle math
    r = 45
    C = 2 * 3.1416 * r
    dash = (score/100) * C

    # Verdict box color
    verdict = info.get("verdict", "Medium Fit")
    vc = "yellow"
    if "Strong" in verdict: vc = "lightgreen"
    if "Weak" in verdict: vc = "red"

    def badges(items, color="rgba(255,255,255,0.08)"):
        if not items:
            return "<div class='bdg'>—</div>"
        html = ""
        for i in items:
            html += f"<div class='bdg' style='background:{color};'>{html_escape.escape(str(i))}</div>"
        return html

    return f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    background: transparent;
    font-family: 'Inter', sans-serif;
    color:white;
}}

.card {{
    width: 100%;
    padding:30px;
    border-radius:20px;
    background:rgba(0,0,8,0.7);
    border:1px solid rgba(255,255,255,0.08);
}}

.flex {{
    display:flex;
    gap:25px;
    flex-wrap:wrap;
}}

.bdg {{
    padding:10px;
    border-radius:12px;
    margin-bottom:8px;
}}

.progress {{
    height:12px;
    background:rgba(255,255,255,0.1);
    width:260px;
    border-radius:10px;
}}
.fill {{
    height:100%;
    border-radius:10px;
    background:linear-gradient(90deg,#bca6ff,#d3baff);
}}

.score svg {{
    width:110px;
    height:110px;
}}
</style>
</head>
<body>

<div class="card">

    <div class="flex">

        <div class="score">
            <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="{r}" stroke="rgba(255,255,255,0.1)" stroke-width="12" fill="none"/>
                <circle cx="60" cy="60" r="{r}" 
                    stroke="url(#grad)" 
                    stroke-width="12"
                    stroke-linecap="round"
                    stroke-dasharray="{dash} {C}"
                    transform="rotate(-90 60 60)" fill="none"/>
                <defs>
                    <linearGradient id="grad">
                        <stop offset="0%" stop-color="#cda8ff"/>
                        <stop offset="100%" stop-color="#f3d4ff"/>
                    </linearGradient>
                </defs>
                <text x="60" y="68" font-size="22" font-weight="700" text-anchor="middle" fill="white">{score}%</text>
            </svg>
        </div>

        <div style="flex:2;">
            <h2>{html_escape.escape(name)}</h2>
            <p style="color:#cfd8ff;">
                Match: <b>{info.get("job_match")}</b> • {html_escape.escape(info.get("reason",""))}
            </p>
            <div style="padding:8px 12px;border-radius:12px;display:inline-block;background:{vc};color:black;font-weight:700;">
                {verdict}
            </div>
        </div>

        <div>
            <h4>Skills</h4>

            <div class="progress"><div class="fill" style="width:{hard}%"></div></div>
            <div>Hard {hard}%</div>

            <br>

            <div class="progress"><div class="fill" style="width:{soft}%"></div></div>
            <div>Soft {soft}%</div>
        </div>

    </div>

    <hr style="margin:25px 0;opacity:0.2;">

    <div class="flex">
        <div>
            <h4>Top Strengths</h4>
            {badges(info.get("strengths", []))}
        </div>

        <div>
            <h4>Top Weaknesses</h4>
            {badges(info.get("weaknesses", []), "rgba(255,0,0,0.25)")}
        </div>

        <div>
            <h4>Missing Keywords</h4>
            {badges(info.get("missing_keywords", []), "rgba(255,50,50,0.25)")}
        </div>
    </div>

</div>

</body>
</html>
"""


# =========================================================
# MAIN UI
# =========================================================
st.title("TalentMatch – AI Resume Screening Agent")

jd = st.text_area("📄 Paste Job Description", height=180)
uploads = st.file_uploader("📂 Upload Resume PDFs", type="pdf", accept_multiple_files=True)


# =========================================================
# PROCESS BUTTON
# =========================================================
if st.button("Generate ATS Reports"):

    if not jd:
        st.error("Please paste the Job Description.")
        st.stop()

    if not uploads:
        st.error("Please upload resume PDFs.")
        st.stop()

    results = []

    for pdf in uploads:
        text = extract_text(pdf)
        st.info(f"Analyzing {pdf.name}...")
        data = call_ai(jd, text)
        if data:
            results.append((pdf.name, data))

    if not results:
        st.error("Failed to generate results.")
        st.stop()

    results.sort(key=lambda x: x[1].get("score", 0), reverse=True)

    st.header("🏆 Candidate Reports")

    for name, info in results:
        st.subheader(name)
        st_html(card(name, info), height=1350, scrolling=True)
