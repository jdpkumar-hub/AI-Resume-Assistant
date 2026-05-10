import streamlit as st

st.title("🚀 AI Resume Assistant")

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="AI Resume Assistant", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f8fafc, #eef2ff);
}

[data-testid="stVerticalBlock"] {
    gap: 1rem;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)


# =============================
# LAYOUT
# =============================
left, right = st.columns([1, 3])

# ================= LEFT PANEL =================
with left:

    st.image("images/logo.png", width=120)

    st.markdown("# 🚀 AI Resume")
    st.markdown("### Assistant")

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        ["Login", "Register", "Reset Password"]
    )

    st.markdown("---")

    st.markdown("""
### ✨ Features

✔ ATS Score Checker  
✔ Resume Rewrite  
✔ Interview Questions  
✔ PDF Download  
✔ AI Optimization  
✔ Resume Templates  
""")

    st.markdown("---")

    st.markdown("""
### 💎 Plans

🆓 Free Plan  
- 3 Resume Analyses

🚀 Pro Plan  
- Unlimited Usage  
- Premium ATS  
- Faster AI
""")

    st.markdown("---")

    st.caption("© 2026 AI Resume Assistant")