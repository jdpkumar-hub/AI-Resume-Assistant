# 📄 STEP 9 — Create pages/2_Register.py
import streamlit as st
from utils.auth import register_user

st.title("📝 Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):

    if register_user(username, password):
        st.success("Registration successful")
    else:
        st.error("User already exists")
