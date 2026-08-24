import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from auth import get_current_user

st.title("🧠 DSA Mentor")
st.subheader("Master Data Structures & Algorithms with AI-Powered Mentoring")

st.markdown("---")

# --- How It Works ---
st.markdown("### 🚀 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1️⃣")
    st.markdown("**Paste Your Question**")
    st.write("Copy any DSA problem from LeetCode, HackerRank, or your own practice")

with col2:
    st.markdown("### 2️⃣")
    st.markdown("**Get AI Nudges**")
    st.write("Start with gentle hints — no spoilers! The AI guides you without giving the answer")

with col3:
    st.markdown("### 3️⃣")
    st.markdown("**Level Up Gradually**")
    st.write("Need more help? Unlock deeper hints: Nudge → Strategy → Structure → Solution")

with col4:
    st.markdown("### 4️⃣")
    st.markdown("**Track Progress**")
    st.write("Earn XP, build streaks, and watch your skills grow on your dashboard")

st.markdown("---")

# --- Features ---
st.markdown("### ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🧠 4-Level AI Mentoring")
    st.write("Progressive hints that teach you to think, not just copy solutions. Powered by Google Gemini AI.")

with col2:
    st.markdown("#### 📊 Smart Dashboard")
    st.write("Track solved problems, difficulty breakdown, topic mastery, and XP history — all in one place.")

with col3:
    st.markdown("#### 🔥 Streaks & XP")
    st.write("Stay motivated with daily streaks, XP rewards, and level progression. The less hints you use, the more XP you earn!")

st.markdown("---")

# --- XP System ---
st.markdown("### 💰 XP Reward System")
st.write("Earn XP based on difficulty. Using fewer hints = more XP!")

xp_data = {
    "Difficulty": ["Easy", "Medium", "Hard"],
    "Base XP": [20, 50, 100],
    "0 Hints": ["20 XP (100%)", "50 XP (100%)", "100 XP (100%)"],
    "Nudge 1": ["18 XP (90%)", "45 XP (90%)", "90 XP (90%)"],
    "Nudge 2": ["15 XP (75%)", "37 XP (75%)", "75 XP (75%)"],
    "Structure": ["10 XP (50%)", "25 XP (50%)", "50 XP (50%)"],
    "Solution": ["4 XP (20%)", "10 XP (20%)", "20 XP (20%)"],
}
st.table(xp_data)

st.markdown("---")

# --- CTA ---
st.markdown("### 🎯 Ready to Start?")
st.write("Create an account and solve your first problem today!")

if get_current_user():
    if st.button("🚀 Start Solving", use_container_width=True):
        st.switch_page("pages/solve_page.py")
else:
    if st.button("🚀 Get Started", use_container_width=True):
        st.rerun()