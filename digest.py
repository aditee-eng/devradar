import os
from groq import Groq
from dotenv import load_dotenv
from database import get_github_history, get_leetcode_history

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_weekly_digest():
    github_history = get_github_history()
    leetcode_history = get_leetcode_history()

    # get this week's data
    github_now = github_history[0] if github_history else None
    leetcode_now = leetcode_history[0] if leetcode_history else None

    # calculate progress vs last week if available
    github_diff = ""
    leetcode_diff = ""

    if len(github_history) >= 2:
        prev = github_history[1]
        curr = github_history[0]
        commit_diff = curr[1] - prev[1]
        github_diff = f"vs last week: {'+' if commit_diff >= 0 else ''}{commit_diff} commits"

    if len(leetcode_history) >= 2:
        prev = leetcode_history[1]
        curr = leetcode_history[0]
        solved_diff = curr[1] - prev[1]
        leetcode_diff = f"vs last week: {'+' if solved_diff >= 0 else ''}{solved_diff} problems solved"

    prompt = f"""
    You are writing a personal weekly engineering digest for a developer.
    Be specific, honest, and encouraging but not fake. 
    Sound like a smart friend who knows their stats, not a corporate newsletter.
    Keep it to 4-5 sentences max.
    
    This week's stats:
    
    GitHub:
    - Commits this week: {github_now[1] if github_now else 0}
    - PRs opened: {github_now[2] if github_now else 0}
    - Active repos: {github_now[3] if github_now else 0}
    {github_diff}
    
    LeetCode:
    - Total solved: {leetcode_now[1] if leetcode_now else 0}
    - Easy/Medium/Hard: {leetcode_now[2] if leetcode_now else 0}/{leetcode_now[3] if leetcode_now else 0}/{leetcode_now[4] if leetcode_now else 0}
    - Current streak: {leetcode_now[5] if leetcode_now else 0} days
    {leetcode_diff}
    
    Write the digest now. Start directly with the insight, no intro like "Here's your digest".
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("\nYour Weekly DevRadar Digest")
    print("=" * 40)
    print(generate_weekly_digest())