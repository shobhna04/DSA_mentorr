import streamlit as st
from supabase_client import get_authenticated_client, get_client

def _db():
    session = st.session_state.get("session")
    if session:
        return get_authenticated_client(session.access_token)
    return get_client()

def create_question(user_id, title, topic, difficulty, problem_statement):
    response = _db().table("questions").insert({
        "user_id": user_id,
        "title": title,
        "topic": topic,
        "difficulty": difficulty,
        "problem_statement": problem_statement
    }).execute()
    return response.data[0] if response.data else None

def get_user_questions(user_id):
    response = _db().table("questions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return response.data

def save_hint(question_id, user_id, tier, hint_text):
    response = _db().table("hints").insert({
        "question_id": question_id,
        "user_id": user_id,
        "tier": tier,
        "hint_text": hint_text
    }).execute()
    return response.data[0] if response.data else None

def get_hints_for_question(question_id):
    response = _db().table("hints").select("*").eq("question_id", question_id).order("tier").execute()
    return response.data

def mark_question_solved(question_id, confidence=None):
    update_data = {"status": "solved"}
    if confidence:
        update_data["confidence"] = confidence
    response = _db().table("questions").update(update_data).eq("id", question_id).execute()
    return response.data

def get_dashboard_stats(user_id):
    questions = _db().table("questions").select("*").eq("user_id", user_id).execute().data
    
    total = len(questions)
    solved = len([q for q in questions if q["status"] == "solved"])
    easy = len([q for q in questions if q["status"] == "solved" and q["difficulty"] == "easy"])
    medium = len([q for q in questions if q["status"] == "solved" and q["difficulty"] == "medium"])
    hard = len([q for q in questions if q["status"] == "solved" and q["difficulty"] == "hard"])
    
    topic_counts = {}
    for q in questions:
        if q["status"] == "solved":
            topic = q["topic"]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    return {
        "total": total, "solved": solved,
        "easy": easy, "medium": medium, "hard": hard,
        "topics": topic_counts
    }
from datetime import date, datetime

def record_solve(user_id, question_id, difficulty, max_hint_tier):
    from gamification import calculate_xp, update_streak
    
    db = _db()
    
    xp = calculate_xp(difficulty, max_hint_tier)
    
    profile = db.table("profiles").select("*").eq("id", user_id).execute().data[0]
    
    today = date.today()
    last_active = None
    if profile.get("last_active_date"):
        last_active = datetime.strptime(profile["last_active_date"], "%Y-%m-%d").date()
    
    streak_info = update_streak(last_active, today)
    
    current_streak = profile.get("current_streak", 0)
    if streak_info["current_streak"] == "increment":
        current_streak += 1
    elif streak_info["current_streak"] is not None:
        current_streak = streak_info["current_streak"]
    
    longest_streak = max(profile.get("longest_streak", 0), current_streak)
    
    db.table("profiles").update({
        "total_xp": profile.get("total_xp", 0) + xp,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_active_date": str(today)
    }).eq("id", user_id).execute()
    
    db.table("questions").update({
        "status": "solved",
        "solved_at": datetime.now().isoformat()
    }).eq("id", question_id).execute()
    
    db.table("xp_transactions").insert({
        "user_id": user_id,
        "amount": xp,
        "source": "question_solve",
        "question_id": question_id
    }).execute()
    
    return {"xp_earned": xp, "current_streak": current_streak, "longest_streak": longest_streak}

def get_profile(user_id):
    return _db().table("profiles").select("*").eq("id", user_id).execute().data[0]

def get_xp_history(user_id):
    return _db().table("xp_transactions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data

def get_daily_activities(user_id):
    return _db().table("daily_activities").select("*").eq("user_id", user_id).order("activity_date", desc=True).execute().data
def get_profile(user_id):
    result = _db().table("profiles").select("*").eq("id", user_id).execute().data
    if result:
        return result[0]
    return {
        "total_xp": 0,
        "current_streak": 0,
        "longest_streak": 0,
        "last_active_date": None
    }