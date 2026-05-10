# 📄 STEP 10 — Create pages/3_Dashboard.py

```python
import streamlit as st

if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

st.title("📄 User Dashboard")

st.write(f"Welcome {st.session_state.user['username']}")

st.info("Your AI Resume tools will appear here")

if st.button("Logout"):
    del st.session_state.user
    st.switch_page("pages/1_Login.py")
```

---