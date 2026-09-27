import streamlit as st
from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title="DSA Mentor",
    page_icon="🧠",
    layout="wide"
)

# --- Hide Streamlit & GitHub branding ---
st.markdown("""
<style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "user" not in st.session_state:
    st.session_state["user"] = None
if "session" not in st.session_state:
    st.session_state["session"] = None

# --- Cookie-based persistent login ---
controller = CookieController()

import time

if st.session_state["user"] is None:
    # CookieController needs a moment to load cookies from browser
    # on first render after refresh, cookies may not be available yet
    if "cookie_checked" not in st.session_state:
        st.session_state["cookie_checked"] = False

    refresh_token = controller.get("dsa_refresh_token")

    # If no token found on first try, wait briefly and rerun once
    if refresh_token is None and not st.session_state["cookie_checked"]:
        st.session_state["cookie_checked"] = True
        time.sleep(0.5)
        st.rerun()

    if refresh_token:
        try:
            from supabase_client import get_client
            supabase = get_client()
            response = supabase.auth.refresh_session(refresh_token)
            if response and response.user:
                st.session_state["user"] = response.user
                st.session_state["session"] = response.session
                # Update cookie with fresh token
                controller.set("dsa_refresh_token", response.session.refresh_token)
                st.session_state["cookie_checked"] = True
                st.rerun()
            else:
                controller.remove("dsa_refresh_token")
        except Exception as e:
            error_msg = str(e).lower()
            if "invalid" in error_msg or "expired" in error_msg or "revoked" in error_msg:
                controller.remove("dsa_refresh_token")

# --- Define all pages ---
login_page = st.Page("pages/page2_auth.py", title="Login", icon="🔐")
homepage = st.Page("pages/homepage.py", title="Homepage", icon="🏠", default=True)
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
revision = st.Page("pages/revision_page.py", title="Revision", icon="📅")
solve = st.Page("pages/solve_page.py", title="Solve", icon="💡")
logout_page = st.Page("pages/logout.py", title="Logout", icon="🚪")

# --- Navigation based on login state ---
if st.session_state["user"]:
    pg = st.navigation(
        {
            "Menu": [homepage, dashboard, revision, solve],
            "Account": [logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()