# 📄 STEP 11 — Create pages/4_Admin.py

import streamlit as st
import pandas as pd
from utils.auth import get_all_users

if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

if not st.session_state.user["is_admin"]:
    st.error("Access denied")
    st.stop()

st.title("🛠 Admin Dashboard")

users = get_all_users()

st.subheader("All Users")

if users:
    df = pd.DataFrame(users)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No users found")
