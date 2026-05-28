import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def strip_markdown(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'#+\s', '', text)
    return text.strip()

def generate_weekly_digest(github: dict, leetcode: dict) -> str:
    prompt = f"""
    You are writing a personal weekly engineering digest for a developer.
    Be specific, honest, and encouraging but not fake.
    Sound like a smart friend who knows their stats, not a corporate newsletter.
    Keep it to 4-5 sentences max.

    GitHub this week:
    - Commits: {github.get('commits_this_week', 0)}
    - PRs opened: {github.get('prs_opened', 0)}
    - Active repos: {github.get('repo_count', 0)}

    LeetCode:
    - Total solved: {leetcode.get('total_solved', 0)}
    - Easy/Medium/Hard: {leetcode.get('easy_solved', 0)}/{leetcode.get('medium_solved', 0)}/{leetcode.get('hard_solved', 0)}
    - Current streak: {leetcode.get('streak', 0)} days
    - Submissions today: {leetcode.get('submissions_today', 0)} attempts

    Write the digest now. Start directly with the insight, no intro.
    If submissions_today > 0, acknowledge that the person was active on LeetCode today.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return strip_markdown(response.choices[0].message.content)