import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from auth import sign_out

st.title("🚪 Logging out...")

if st.session_state.get("user"):
    sign_out()
    st.rerun()
else:
    st.info("You are already logged out.")
