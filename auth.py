import streamlit as st
from supabase_client import get_client

supabase = get_client()

def sign_up(email, password, username):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"username": username}
            }
        })
        # Auto-create profile for the new user
        if response.user:
            try:
                supabase.table("profiles").upsert({
                    "id": response.user.id,
                    "total_xp": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "last_active_date": None
                }).execute()
            except Exception:
                pass  # Profile might already exist or table has a trigger
        return {"success": True, "user": response.user}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state["user"] = response.user
        st.session_state["session"] = response.session
        # Ensure profile exists for this user
        if response.user:
            try:
                supabase.table("profiles").upsert({
                    "id": response.user.id,
                    "total_xp": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "last_active_date": None
                }, on_conflict="id", ignore_duplicates=True).execute()
            except Exception:
                pass
        return {"success": True, "user": response.user}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.pop("user", None)
        st.session_state.pop("session", None)
    except Exception as e:
        pass

def get_current_user():
    return st.session_state.get("user", None)