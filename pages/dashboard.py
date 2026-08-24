import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from auth import get_current_user
from database import get_dashboard_stats, get_profile, get_user_questions, get_xp_history, get_daily_activities
from gamification import calculate_level, get_level_progress, xp_for_level

# Auth guard
if not get_current_user():
    st.warning("Please login first! 🔐")
    st.stop()

st.title("📊 Your Dashboard")

user = get_current_user()
profile = get_profile(user.id)
stats = get_dashboard_stats(user.id)

# ===========================
# ROW 1: Metric Cards
# ===========================
col1, col2, col3, col4 = st.columns(4)

total_xp = profile.get("total_xp", 0)
level = calculate_level(total_xp)

with col1:
    st.metric("🏆 Total XP", f"{total_xp} XP")
with col2:
    st.metric("📈 Level", level)
with col3:
    st.metric("✅ Solved", stats["solved"])
with col4:
    st.metric("🔥 Streak", f"{profile.get('current_streak', 0)} days")

# Level progress bar
progress = get_level_progress(total_xp)
next_level_xp = xp_for_level(level + 1)
st.progress(progress, text=f"Level {level} → Level {level + 1}  ({total_xp}/{next_level_xp} XP)")

st.divider()

# ===========================
# ROW 2: Charts
# ===========================
col_left, col_right = st.columns(2)

# Difficulty Donut Chart
with col_left:
    st.subheader("🍩 Difficulty Breakdown")
    labels = ["Easy", "Medium", "Hard"]
    values = [stats["easy"], stats["medium"], stats["hard"]]
    colors = ["#00CC66", "#FFAA00", "#FF4444"]

    if sum(values) > 0:
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors),
            textinfo="label+value"
        )])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            showlegend=False,
            height=300,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Solve some problems to see your breakdown!")

# Topic Bar Chart
with col_right:
    st.subheader("📊 Topics Mastered")
    topics = stats.get("topics", {})

    if topics:
        fig = go.Figure(data=[go.Bar(
            x=list(topics.values()),
            y=list(topics.keys()),
            orientation="h",
            marker=dict(color="#6C63FF")
        )])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=300,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis_title="Problems Solved"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Solve some problems to see your topics!")

st.divider()

# ===========================
# ROW 3: Streak & XP Info
# ===========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Streak Info")
    st.write(f"**Current Streak:** {profile.get('current_streak', 0)} days")
    st.write(f"**Longest Streak:** {profile.get('longest_streak', 0)} days")

with col2:
    st.subheader("💰 Recent XP")
    xp_history = get_xp_history(user.id)
    if xp_history:
        for tx in xp_history[:5]:
            st.write(f"+{tx['amount']} XP — {tx['source']} — {tx['created_at'][:10]}")
    else:
        st.info("No XP earned yet!")

st.divider()

# ===========================
# ROW 4: Recent Activity
# ===========================
st.subheader("📋 Recent Questions")
questions = get_user_questions(user.id)

if questions:
    for q in questions[:10]:
        status_icon = "✅" if q["status"] == "solved" else "🔄"
        st.write(f"{status_icon} **{q['title']}** — {q['topic']} — {q['difficulty']} — {q['created_at'][:10]}")
else:
    st.info("No questions yet! Go solve some problems 💪")