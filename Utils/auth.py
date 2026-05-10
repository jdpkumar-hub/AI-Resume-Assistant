from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ======================================
# REGISTER
# ======================================
def register_user(username, email, password):

    existing = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if existing.data:
        return False

    supabase.table("users").insert({
        "username": username,
        "email": email,
        "password": password,
        "is_admin": False,
        "is_pro": False,
        "usage": 0
    }).execute()

    return True

# ======================================
# LOGIN
# ======================================
def login_user(username, password):

    result = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .eq("password", password) \
        .execute()

    if result.data:
        return result.data[0]

    return None

# ======================================
# RESET PASSWORD
# ======================================
def reset_password(username, new_password):

    result = supabase.table("users") \
        .update({"password": new_password}) \
        .eq("username", username) \
        .execute()

    return True