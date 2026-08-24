import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.2
        }
    )
    
    return response.text
