import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from auth import sign_up, sign_in, get_current_user

# If already logged in, go to homepage
if get_current_user():
    st.rerun()

st.title("🔐 Login / Sign Up")

login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

# --- LOGIN TAB ---
with login_tab:
    st.subheader("Welcome back!")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn", use_container_width=True):
        if not login_email or not login_password:
            st.error("Please fill in all fields!")
        else:
            with st.spinner("Logging in..."):
                result = sign_in(login_email, login_password)
            if result["success"]:
                st.success("Logged in! 🎉")
                st.balloons()
                st.rerun()
            else:
                st.error(f"Login failed: {result['error']}")

# --- SIGNUP TAB ---
with signup_tab:
    st.subheader("Create your account")
    signup_username = st.text_input("Username", key="signup_username")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up", key="signup_btn", use_container_width=True):
        if not signup_username or not signup_email or not signup_password:
            st.error("Please fill in all fields!")
        elif len(signup_password) < 6:
            st.error("Password must be at least 6 characters!")
        else:
            with st.spinner("Creating account..."):
                result = sign_up(signup_email, signup_password, signup_username)
            if result["success"]:
                st.success("Account created! ✅ You can now login.")
            else:
                st.error(f"Signup failed: {result['error']}")