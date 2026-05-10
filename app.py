import streamlit as st
import json
import os
import io
import stripe
from openai import OpenAI
from docx import Document
import pdfplumber
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="AI Resume Assistant", layout="wide")

# 🔐 USE ENV VARIABLES
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
PRICE_ID = st.secrets["PRICE_ID"]
SUCCESS_URL = st.secrets["SUCCESS_URL"]
CANCEL_URL = st.secrets["CANCEL_URL"]

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

def register(username, password):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": password,
        "is_pro": False,
        "usage": 0
    }

    save_users(users)
    return True

def login(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

# =============================
def reset_password(username, new_password):
    users = load_users()

    if username not in users:
        return False

    users[username]["password"] = new_password
    save_users(users)

    return True
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
# PAYMENT SUCCESS HANDLER
# =============================
query_params = st.query_params

if "success" in query_params and st.session_state.user:
    users = load_users()
    users[st.session_state.user]["is_pro"] = True
    save_users(users)
    st.success("🎉 Payment successful! Pro unlocked.")

# =============================
# AUTH UI
# =============================
if not st.session_state.user:

    st.title("🚀 AI Resume Assistant")

    st.markdown("""
### Get Hired Faster with AI

✔ Resume Optimization  
✔ ATS Score Analysis  
✔ Interview Preparation  
✔ AI Resume Rewrite  
""")

    menu = st.radio("Choose", ["Login", "Register", "Reset Password"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":

        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif menu == "Register":

        if st.button("Register"):
            if register(username, password):
                st.success("Registered! Please login")
            else:
                st.error("User already exists")

    elif menu == "Reset Password":

        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if reset_password(username, new_password):
                st.success("Password updated successfully!")
            else:
                st.error("Username not found")
    st.stop()
# =============================
# USER DATA
# =============================
users = load_users()
user_data = users[st.session_state.user]

# =============================
# SIDEBAR
# =============================
st.sidebar.write(f"👤 {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("## 💎 Plan")

if user_data["is_pro"]:
    st.sidebar.success("Pro User ✅")
else:
    st.sidebar.warning("Free Plan")
    st.sidebar.write(f"Usage: {user_data['usage']}/3")

# =============================
# USAGE LIMIT
# =============================
FREE_LIMIT = 3

if not user_data["is_pro"] and user_data["usage"] >= FREE_LIMIT:
    st.warning("Free limit reached 🚀 Upgrade to Pro")

    if st.button("Upgrade to Pro"):
        checkout = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            mode="subscription",
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
        )

        st.markdown(f"[👉 Click here to pay]({checkout.url})")

    st.stop()

# =============================
# MAIN UI
# =============================
st.title("📄 AI Resume Assistant")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
resume_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

if st.button("Analyze Resume"):

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

        st.success("Done!")

        st.subheader("📊 ATS Score")
        st.write(ats)

        st.subheader("📄 Improved Resume")
        st.write(improved)

        pdf = generate_pdf(improved)
        st.download_button("Download Resume PDF", pdf, "resume.pdf")

        st.subheader("🎯 Interview Questions")
        st.write(questions)

        # ✅ INCREMENT USAGE
        users[st.session_state.user]["usage"] += 1
        save_users(users)