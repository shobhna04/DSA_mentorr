import streamlit as st
from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title="DSA Mentor",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if "user" not in st.session_state:
    st.session_state["user"] = None
if "session" not in st.session_state:
    st.session_state["session"] = None

# --- Cookie-based persistent login ---
controller = CookieController()

if st.session_state["user"] is None:
    refresh_token = controller.get("dsa_refresh_token")
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
                st.rerun()
        except Exception:
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