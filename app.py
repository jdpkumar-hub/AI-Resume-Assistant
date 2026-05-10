import streamlit as st
from utils.auth import (
    register_user,
    login_user,
    reset_password
)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Resume Assistant",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

/* Main background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f8fafc, #eef2ff);
}

/* Reduce top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}

/* Column spacing */
[data-testid="column"] {
    padding: 1.5rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 25px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
}

/* Buttons */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
    font-weight: bold;
    width: 100%;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Inputs */
.stTextInput input {
    border-radius: 10px;
}

/* Hide Streamlit menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = None


# ==========================================
# LAYOUT
# ==========================================
left, right = st.columns([1, 2.2])

# ==========================================
# LEFT PANEL
# ==========================================
with left:

    st.image("images/logo.png", width=140)

    st.markdown("""
    <h1 style='margin-bottom:0;color:#111827;'>
    AI Resume Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color:gray;font-size:18px;'>
    🚀 Smart Career Optimization
    </p>
    """, unsafe_allow_html=True)
# ==========================================
# DUMMY AUTH FUNCTIONS
# Replace later with Supabase
# ==========================================
if st.button("Login"):

    user = login_user(username, password)

    if user:
        st.session_state.user = user
        st.success("Login successful ✅")
        st.rerun()

    else:
        st.error("Invalid credentials")
        

if st.button("Create Account"):

    if register_user(
        reg_user,
        reg_email,
        reg_pass
    ):
        st.success("Registration successful ✅")

    else:
        st.error("User already exists")
        
        
if st.button("Reset Password"):

    if reset_password(reset_user, reset_pass):
        st.success("Password updated ✅")

    else:
        st.error("User not found")
    st.markdown("---")

    st.markdown("""
    ### ✨ Features

    ✔ ATS Score Checker  
    ✔ Resume Rewrite  
    ✔ Interview Questions  
    ✔ PDF Export  
    ✔ AI Optimization  
    ✔ Resume Templates  
    """)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("---")


    st.caption("Built by JDP Kumar 🚀")

# ==========================================
# RIGHT PANEL
# ==========================================
with right:

    st.markdown("""
    <h1 style='text-align:center;color:#111827;'>
    🤖 AI Resume Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================
    # TABS
    # ======================================
    tab1, tab2, tab3 = st.tabs([
        "🔐 Login",
        "🆕 Signup",
        "🔑 Reset"
    ])

    # ======================================
    # LOGIN TAB
    # ======================================
    with tab1:

        st.markdown("### Welcome Back 👋")

        username = st.text_input(
            "Email / Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login"):

            if login(username, password):
                st.session_state.user = username
                st.success("Login successful ✅")
            else:
                st.error("Invalid credentials")

        st.markdown("<br>", unsafe_allow_html=True)

        st.info("Demo Login → admin / admin")

    # ======================================
    # REGISTER TAB
    # ======================================
    with tab2:

        st.markdown("### Create Account 🚀")

        reg_user = st.text_input(
            "Username",
            key="reg_user"
        )

        reg_email = st.text_input(
            "Email",
            key="reg_email"
        )

        reg_pass = st.text_input(
            "Password",
            type="password",
            key="reg_pass"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Create Account"):

            if register(reg_user, reg_pass):
                st.success("Registration successful ✅")
            else:
                st.error("User already exists")

    # ======================================
    # RESET PASSWORD TAB
    # ======================================
    with tab3:

        st.markdown("### Reset Password 🔑")

        reset_user = st.text_input(
            "Username",
            key="reset_user"
        )

        reset_pass = st.text_input(
            "New Password",
            type="password",
            key="reset_pass"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Reset Password"):

            if reset_password(reset_user, reset_pass):
                st.success("Password updated ✅")
            else:
                st.error("User not found")

# ==========================================
# AFTER LOGIN
# ==========================================
if st.session_state.user:

    st.markdown("---")

    st.success(f"Welcome {st.session_state.user} 🚀")

    st.write("Your dashboard will appear here.")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()