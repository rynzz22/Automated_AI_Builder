import os
from pathlib import Path

from google import genai

# =====================================================================
# CONFIGURATION
# =====================================================================
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("Set the GEMINI_API_KEY environment variable before running this script.")

client = genai.Client(api_key=GEMINI_KEY)

MODEL_ID = "gemini-3.6-flash"
OUTPUT_PATH = Path(__file__).with_name("generated_output.txt")

PROMPTER_SYSTEM_PROMPT = (
    "You are an elite Product Manager and Technical Architect. Your job is to take a high-level software goal "
    "or developer code feedback and translate it into a strict, highly detailed markdown specification prompt "
    "that a developer AI can execute. Focus on edge cases, user experience, and structure. Do not write code yourself. "
    "Respond ONLY with the technical developer prompt instruction. Do not use emojis."
)

DEVELOPER_SYSTEM_PROMPT = (
    "You are a Senior Full-Stack Software Engineer. Your job is to read technical specifications and write "
    "clean, robust, production-ready, fully commented code. Never use placeholder comments like '// add logic here'. "
    "Write out the entire implementation completely so it can be saved directly to a file. Do not use emojis."
)

def ask_prompter(user_input):
    """Uses Gemini as the Architect/Prompter."""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_input,
            config={'system_instruction': PROMPTER_SYSTEM_PROMPT}
        )
        return response.text or ""
    except Exception as e:
        return f"ERROR: Prompter request failed: {e}"

def ask_developer(technical_prompt):
    """Uses Gemini as the Engineer/Coder."""
    if technical_prompt.startswith("ERROR:"):
        return f"Developer skipped because Prompter step failed:\n{technical_prompt}"
        
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=technical_prompt,
            config={'system_instruction': DEVELOPER_SYSTEM_PROMPT}
        )
        return response.text or ""
    except Exception as e:
        return f"ERROR: Developer request failed: {e}"

def run_collaboration_loop(project_goal, total_rounds=2):
    if not project_goal.strip():
        raise ValueError("project_goal must not be empty.")
    if total_rounds < 1:
        raise ValueError("total_rounds must be at least 1.")

    print(f"Project Goal: '{project_goal}'")
    print(f"Prompter Role Model: {MODEL_ID}")
    print(f"Developer Role Model: {MODEL_ID}\n")
    
    current_input = project_goal
    latest_code = ""

    for round_num in range(1, total_rounds + 1):
        print(f"--- ROUND {round_num} OF {total_rounds} ---")
        
        print("Prompter is architecting the technical requirements...")
        architect_spec = ask_prompter(current_input)
        print(f"Specification generated ({len(architect_spec)} characters).\n")
        
        print("Developer is engineering the source code...")
        latest_code = ask_developer(architect_spec)
        print(f"Code built ({len(latest_code)} characters).\n")
        
        if round_num < total_rounds:
            print("Prompter is reviewing the generated code for enhancements...")
            current_input = (
                f"The developer built this code based on your last prompt:\n\n{latest_code}\n\n"
                f"Analyze this code. Identify any bugs, missing logical features, or styling flaws. "
                f"Now, generate a brand new, updated technical prompt telling the developer exactly "
                f"how to rewrite the code to fix these specific problems."
            )
            print("Feedback loaded for the next round.\n")

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(latest_code)
        
    print(f"Collaboration complete. Final project codebase saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    my_app_idea = "A sleek HTML/CSS/JS digital clock with an integrated countdown stopwatch and dark mode toggle."
    run_collaboration_loop(project_goal=my_app_idea, total_rounds=2)