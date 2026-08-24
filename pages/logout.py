import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from streamlit_cookies_controller import CookieController
from auth import sign_out

controller = CookieController()

st.title("🚪 Logging out...")

if st.session_state.get("user"):
    # Clear the login cookie first
    controller.remove("dsa_refresh_token")
    sign_out()
    st.rerun()
else:
    st.info("You are already logged out.")
