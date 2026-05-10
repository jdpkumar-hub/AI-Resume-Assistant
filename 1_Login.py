# 📄 STEP 8 — Create pages/1_Login.py

import streamlit as st
from utils.auth import login_user

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    user = login_user(username, password)

    if user:
        st.session_state.user = user
        st.success("Login successful")

        if user["is_admin"]:
            st.switch_page("pages/4_Admin.py")
        else:
            st.switch_page("pages/3_Dashboard.py")

    else:
        st.error("Invalid credentials")

