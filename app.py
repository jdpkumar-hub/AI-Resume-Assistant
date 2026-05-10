import streamlit as st

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

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f8fafc, #eef2ff);
}

.block-container {
    padding-top: 1.5rem;
}

[data-testid="column"] {
    padding: 1rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
}

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

.stTextInput input {
    border-radius: 10px;
}

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
# SESSION
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = None

# ==========================================
# DEMO AUTH
# Replace later with Supabase
# ==========================================
def login(username, password):
    return username == "admin" and password == "admin"


def register(username, email, password):
    return True


def reset_password(username, new_password):
    return True

# ==========================================
# MAIN LAYOUT
# ==========================================
left, right = st.columns([1, 2])

# ==========================================
# LEFT PANEL
# ==========================================
with left:

    st.image("images/logo.png", width=120)

    st.markdown("""
    <h1 style='margin-bottom:0;'>
    AI Resume Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color:gray;font-size:18px;'>
    🚀 Smart Career Optimization
    </p>
    """, unsafe_allow_html=True)

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

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🤖 AI Resume Assistant
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================
    # TABS
    # ======================================
    login_tab, signup_tab, reset_tab = st.tabs([
        "🔐 Login",
        "🆕 Signup",
        "🔑 Reset"
    ])

    # ======================================
    # LOGIN TAB
    # ======================================
    with login_tab:

        st.markdown("### Welcome Back 👋")

        login_user = st.text_input(
            "Username",
            key="login_user"
        )

        login_pass = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login", key="login_btn"):

            if login(login_user, login_pass):
                st.session_state.user = login_user
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # ======================================
    # SIGNUP TAB
    # ======================================
    with signup_tab:

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

        if st.button(
            "Create Account",
            key="register_btn"
        ):

            if register(reg_user, reg_email, reg_pass):
                st.success("Registration successful ✅")
            else:
                st.error("User already exists")

    # ======================================
    # RESET TAB
    # ======================================
    with reset_tab:

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

        if st.button(
            "Reset Password",
            key="reset_btn"
        ):

            if reset_password(reset_user, reset_pass):
                st.success("Password updated ✅")
            else:
                st.error("User not found")

# ==========================================
# AFTER LOGIN
# ==========================================
if st.session_state.user:

    st.markdown("---")

    st.success(
        f"Welcome {st.session_state.user} 🚀"
    )

    st.subheader("📄 Dashboard")

    st.info(
        "Resume upload, ATS analysis, and AI tools will appear here."
    )

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.rerun()

