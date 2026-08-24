import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from datetime import date, timedelta
from auth import get_current_user

# Auth guard
if not get_current_user():
    st.warning("Please login first! 🔐")
    st.stop()

st.title("📅 Revision Schedule")
st.write("Spaced repetition helps you remember what you've learned!")

user = get_current_user()

from supabase_client import get_client
from database import _db

db = _db()

# --- Get revisions due today ---
today = str(date.today())

due_reviews = db.table("revision_schedule")\
    .select("*, questions(title, topic, difficulty)")\
    .eq("user_id", user.id)\
    .lte("next_review_date", today)\
    .execute().data

upcoming_reviews = db.table("revision_schedule")\
    .select("*, questions(title, topic, difficulty)")\
    .eq("user_id", user.id)\
    .gt("next_review_date", today)\
    .order("next_review_date")\
    .execute().data

# --- Due Today ---
st.subheader(f"🔴 Due Today ({len(due_reviews)})")

if due_reviews:
    for rev in due_reviews:
        question = rev.get("questions", {})
        with st.expander(f"📌 {question.get('title', 'Unknown')} — {question.get('topic', '')} — {question.get('difficulty', '')}", expanded=True):
            st.write(f"**Review count:** {rev['review_count']}")
            st.write(f"**Current interval:** {rev['interval_days']} days")

            if st.button(f"✅ Reviewed!", key=f"review_{rev['id']}"):
                new_interval = rev["interval_days"] * 2
                new_date = str(date.today() + timedelta(days=new_interval))

                db.table("revision_schedule").update({
                    "review_count": rev["review_count"] + 1,
                    "interval_days": new_interval,
                    "next_review_date": new_date
                }).eq("id", rev["id"]).execute()

                st.success(f"✅ Next review in {new_interval} days ({new_date})")
                st.rerun()
else:
    st.success("🎉 No revisions due today! You're all caught up!")

st.divider()

# --- Upcoming ---
st.subheader(f"📅 Upcoming Reviews ({len(upcoming_reviews)})")

if upcoming_reviews:
    for rev in upcoming_reviews:
        question = rev.get("questions", {})
        st.write(f"📌 **{question.get('title', 'Unknown')}** — Due: **{rev['next_review_date']}** — Interval: {rev['interval_days']} days")
else:
    st.info("No upcoming reviews. Solve problems and they'll be scheduled automatically!")

st.divider()

# --- Schedule a revision manually ---
st.subheader("➕ Schedule a Revision")

questions = db.table("questions")\
    .select("id, title")\
    .eq("user_id", user.id)\
    .eq("status", "solved")\
    .execute().data

if questions:
    question_options = {q["title"]: q["id"] for q in questions}
    selected = st.selectbox("Select a solved question", list(question_options.keys()))
    days = st.number_input("Review in how many days?", min_value=1, max_value=90, value=7)

    if st.button("📅 Schedule Review"):
        db.table("revision_schedule").insert({
            "question_id": question_options[selected],
            "user_id": user.id,
            "next_review_date": str(date.today() + timedelta(days=days)),
            "interval_days": days
        }).execute()
        st.success(f"✅ Revision scheduled for {date.today() + timedelta(days=days)}")
        st.rerun()
else:
    st.info("Solve some problems first, then you can schedule revisions!")