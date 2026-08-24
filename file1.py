import streamlit as st

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

# --- Define all pages ---
login_page = st.Page("pages/page2_auth.py", title="Login", icon="🔐")
homepage = st.Page("pages/homepage.py", title="Homepage", icon="🏠", default=True)
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
revision = st.Page("pages/revision_page.py", title="Revision", icon="📅")
solve = st.Page("pages/solve_page.py", title="Solve", icon="💡")
logout_page = st.Page("pages/logout.py", title="Logout", icon="🚪")

# --- Navigation based on login state ---
if st.session_state["user"]:
    # Logged in → show these pages in sidebar
    pg = st.navigation(
        {
            "Menu": [homepage, dashboard, revision, solve],
            "Account": [logout_page],
        }
    )
else:
    # Not logged in → show only login page
    pg = st.navigation([login_page])

pg.run()