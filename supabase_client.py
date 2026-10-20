import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Try st.secrets first (Streamlit Cloud), then fall back to os.environ (local .env)
def _get_secret(key):
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.environ.get(key)

SUPABASE_URL = _get_secret("SUPABASE_URL")
SUPABASE_ANON_KEY = _get_secret("SUPABASE_ANON_KEY")

# Debug: show if secrets loaded (remove after fixing)
import logging
logging.info(f"SUPABASE_URL loaded: {SUPABASE_URL is not None and len(str(SUPABASE_URL)) > 0}")
logging.info(f"SUPABASE_URL value starts with: {str(SUPABASE_URL)[:20] if SUPABASE_URL else 'NONE'}")

def get_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        st.error(f"⚠️ Supabase not configured! URL={'set' if SUPABASE_URL else 'MISSING'}, KEY={'set' if SUPABASE_ANON_KEY else 'MISSING'}. Add secrets in Streamlit Cloud Settings.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_authenticated_client(access_token) -> Client:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client