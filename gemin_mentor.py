import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Try st.secrets first (Streamlit Cloud), then fall back to os.environ (local .env)
def _get_secret(key):
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.environ.get(key)

client = genai.Client(api_key=_get_secret("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert DSA (Data Structures & Algorithms) Mentor. 
Your job is to help students solve coding problems using Socratic mentoring.

You must strictly follow the hint level requested:

LEVEL 1 - Nudge 1: 
- Ask a probing question about the problem
- Hint at what edge cases to think about
- Do NOT name any algorithm or data structure
- Keep it short (2-3 sentences)

LEVEL 2 - Nudge 2:
- Name the algorithmic pattern (e.g. "Two Pointers", "Dynamic Programming")
- Explain WHY this pattern fits
- Do NOT write any code or pseudocode

LEVEL 3 - Structured Approach:
- Give step-by-step pseudocode
- List the variables to track
- Explain the loop logic and termination condition
- Do NOT write actual code

LEVEL 4 - Full Solution:
- Provide complete, clean, commented code
- Explain the time and space complexity
- Walk through the solution line by line
"""

def generate_hint(question_title, problem_statement, hint_level, previous_hints=None):
    level_names = {
        1: "LEVEL 1 - Nudge 1",
        2: "LEVEL 2 - Nudge 2", 
        3: "LEVEL 3 - Structured Approach",
        4: "LEVEL 4 - Full Solution"
    }
    
    prompt = f"""
Question: {question_title}

Problem:
{problem_statement}

Previously given hints:
{previous_hints if previous_hints else "None"}

Please provide: {level_names[hint_level]}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.2
            }
        )
        return response.text
    except Exception as e:
        return f"⚠️ AI hint generation failed: {str(e)}. Please try again."

