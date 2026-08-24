import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from auth import get_current_user
from database import create_question, save_hint, get_hints_for_question, mark_question_solved
from gemin_mentor import generate_hint

# --- Auth Guard ---
if not get_current_user():
    st.warning("Please login first! 🔐")
    st.stop()

st.title("💡 Solve a DSA Problem")

user = get_current_user()

# --- Initialize Session State ---
if "current_question_id" not in st.session_state:
    st.session_state["current_question_id"] = None
if "hints" not in st.session_state:
    st.session_state["hints"] = {}
if "max_tier" not in st.session_state:
    st.session_state["max_tier"] = 0

# ===========================
# SECTION 1: Question Input
# ===========================
if st.session_state["current_question_id"] is None:
    st.subheader("📝 Paste Your DSA Question")

    title = st.text_input("Question Title", placeholder="e.g. Two Sum")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("Topic", [
            "Arrays", "Strings", "Linked List", "Stack", "Queue",
            "Trees", "Graphs", "Dynamic Programming", "Recursion",
            "Binary Search", "Two Pointers", "Sliding Window",
            "Greedy", "Backtracking", "Heap", "Hashing", "Other"
        ])
    with col2:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

    problem_statement = st.text_area(
        "Problem Statement",
        height=200,
        placeholder="Paste the full problem description here..."
    )

    if st.button("🚀 Start Session", use_container_width=True):
        if not title or not problem_statement:
            st.error("Please fill in the title and problem statement!")
        else:
            question = create_question(user.id, title, topic, difficulty, problem_statement)
            if question:
                st.session_state["current_question_id"] = question["id"]
                st.session_state["current_question"] = question
                st.session_state["hints"] = {}
                st.session_state["max_tier"] = 0
                st.success("Session started! 🎯")
                st.rerun()
            else:
                st.error("Failed to create session. Try again.")

# ===========================
# SECTION 2: Hint Panel
# ===========================
else:
    question = st.session_state["current_question"]

    # Show question info
    st.markdown(f"### 📌 {question['title']}")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Topic:** {question['topic']}")
    col2.markdown(f"**Difficulty:** {question['difficulty'].upper()}")
    col3.markdown(f"**Status:** {'✅ Solved' if question.get('status') == 'solved' else '🔄 In Progress'}")

    with st.expander("View Problem Statement", expanded=False):
        st.write(question["problem_statement"])

    st.divider()

    # --- Progress Bar ---
    tier_names = {1: "💡 Nudge 1", 2: "💡 Nudge 2", 3: "📋 Structure", 4: "✅ Solution"}
    progress_cols = st.columns(4)
    for i, (tier, name) in enumerate(tier_names.items()):
        with progress_cols[i]:
            if tier in st.session_state["hints"]:
                st.success(name)
            elif tier == st.session_state["max_tier"] + 1:
                st.info(name)
            else:
                st.empty()

    st.divider()

    # --- XP Warning ---
    xp_warnings = {
        1: "⚠️ Using Nudge 1 reduces XP by 10%",
        2: "⚠️ Using Nudge 2 reduces XP by 25%",
        3: "⚠️ Using Structure reduces XP by 50%",
        4: "⚠️ Using Solution reduces XP by 80%"
    }

    # --- Hint Buttons ---
    next_tier = st.session_state["max_tier"] + 1

    if next_tier <= 4 and question.get("status") != "solved":
        st.warning(xp_warnings[next_tier])

        if st.button(f"Get {tier_names[next_tier]}", use_container_width=True):
            with st.spinner("🧠 AI is thinking..."):
                # Collect previous hints
                prev = "\n".join([
                    f"Tier {t}: {h}" for t, h in st.session_state["hints"].items()
                ])

                # Call Gemini
                response = generate_hint(
                    question["title"],
                    question["problem_statement"],
                    next_tier,
                    prev if prev else None
                )

                # Save hint
                save_hint(
                    question["id"],
                    user.id,
                    next_tier,
                    response
                )

                st.session_state["hints"][next_tier] = response
                st.session_state["max_tier"] = next_tier
                st.rerun()

    # --- Display All Hints ---
    for tier in range(1, 5):
        if tier in st.session_state["hints"]:
            with st.expander(f"{tier_names[tier]}", expanded=(tier == st.session_state["max_tier"])):
                st.markdown(st.session_state["hints"][tier])

    st.divider()

    # --- Mark as Solved ---
    if question.get("status") != "solved":
        st.subheader("✅ Done solving?")
        confidence = st.slider("How confident are you? (1-5)", 1, 5, 3)

        if st.button("🎉 Mark as Solved!", use_container_width=True):
            mark_question_solved(question["id"], confidence)
            st.session_state["current_question"]["status"] = "solved"
            st.balloons()
            st.success(f"Congratulations! Problem solved! 🎉")

    # --- New Question Button ---
    if st.button("📝 Start New Question"):
        st.session_state["current_question_id"] = None
        st.session_state["current_question"] = None
        st.session_state["hints"] = {}
        st.session_state["max_tier"] = 0
        st.rerun()