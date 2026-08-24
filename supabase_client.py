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

def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_authenticated_client(access_token) -> Client:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client