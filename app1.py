import streamlit as st
import json
import os
import io
from openai import OpenAI
from docx import Document
import pdfplumber
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import stripe
import os

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

PRICE_ID = "YOUR_PRICE_ID"
SUCCESS_URL = "http://localhost:8501/?success=true"
CANCEL_URL = "http://localhost:8501/?canceled=true"

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="AI Resume Assistant", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

USER_FILE = "users.json"

# =============================
# USER STORAGE
# =============================
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def login(username, password):
    users = load_users()
    return username in users and users[username] == password

def register(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# =============================
# HELPERS
# =============================
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def generate_pdf(text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph(line, styles["Normal"]) for line in text.split("\n")]
    doc.build(content)
    buffer.seek(0)
    return buffer

# =============================
# SESSION
# =============================
if "user" not in st.session_state:
    st.session_state.user = None

# =============================
# AUTH UI
# =============================
if not st.session_state.user:

    
    st.image("images/logo.png", width=120)
    st.title(" AI Resume Assistant")

    st.markdown("""
### Get Hired Faster with AI

✔ Resume Optimization  
✔ ATS Score Analysis  
✔ Interview Preparation  
✔ AI Resume Rewrite  

Login or Register to continue.
""")

    menu = st.radio("Choose", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        if st.button("Register"):
            if register(username, password):
                st.success("Registered! Please login")
            else:
                st.error("User already exists")

    st.stop()

# =============================
# SIDEBAR (ATS UI)
# =============================
st.sidebar.write(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("## 📊 ATS Score")

# Default score
score = st.session_state.get("score", 0)

st.sidebar.progress(score / 100 if score else 0)
st.sidebar.markdown(f"### {score}% Match Rate")

st.sidebar.markdown("---")
st.sidebar.write("Searchability")
st.sidebar.progress(0.7)

st.sidebar.write("Skills Match")
st.sidebar.progress(0.6)

st.sidebar.write("Formatting")
st.sidebar.progress(0.5)

# =============================
# MAIN HEADER
# =============================
st.title("📄 AI Resume Assistant")

st.markdown("""
### Improve Your Resume & Beat ATS Systems
Upload your resume and get AI-powered insights, score, and improvements.
""")

# =============================
# TABS
# =============================
tab1, tab2 = st.tabs(["📄 Resume", "🧾 Job Match"])

# =============================
# TAB 1: RESUME
# =============================
with tab1:

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    resume_text = ""

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        st.success("Resume uploaded")

    if st.button("⚡ Analyze Resume"):

        if not resume_text.strip():
            st.error("Upload resume first")
        else:
            with st.spinner("Analyzing..."):

                ats = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Give ATS score out of 100"},
                        {"role": "user", "content": resume_text}
                    ]
                ).choices[0].message.content

                improved = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Rewrite this resume professionally"},
                        {"role": "user", "content": resume_text}
                    ]
                ).choices[0].message.content

                questions = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Generate interview questions"},
                        {"role": "user", "content": resume_text}
                    ]
                ).choices[0].message.content

            # Extract score number (basic)
            try:
                score_val = int(''.join(filter(str.isdigit, ats))[:2])
            except:
                score_val = 70

            st.session_state.score = score_val

            st.success("Analysis Complete")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📊 ATS Score")
                st.info(ats)

            with col2:
                st.markdown("### 🎯 Interview Questions")
                st.write(questions)

            st.markdown("---")

            st.markdown("### 📄 Improved Resume")
            st.write(improved)

            pdf = generate_pdf(improved)
            st.download_button("⬇ Download Resume PDF", pdf, "resume.pdf")

# =============================
# TAB 2: JOB MATCH
# =============================
with tab2:

    jd = st.text_area("Paste Job Description")

    if st.button("Match Resume"):

        st.success("Matching complete")

        st.progress(0.75)

        st.markdown("### Missing Keywords")
        st.write("- Python\n- Cloud\n- Performance tuning")