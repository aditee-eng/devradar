import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from github_fetcher import get_github_activity
from leetcode_fetcher import get_leetcode_activity
from digest import generate_weekly_digest
from datetime import datetime, timedelta

# simple in-memory cache
cache = {}
CACHE_DURATION = timedelta(hours=1)

def get_cached(key):
    if key in cache:
        data, timestamp = cache[key]
        if datetime.now() - timestamp < CACHE_DURATION:
            return data
    return None

def set_cached(key, data):
    cache[key] = (data, datetime.now())

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    github_username = request.args.get("github")
    leetcode_username = request.args.get("leetcode")

    if not github_username or not leetcode_username:
        return jsonify({"error": "Missing github or leetcode username"}), 400

    cache_key = f"{github_username}:{leetcode_username}"
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)

    github = get_github_activity(github_username)
    leetcode = get_leetcode_activity(leetcode_username)

    if github.get("error"):
        return jsonify({"error": f"GitHub user '{github_username}' not found. Check your username."}), 404

    if leetcode.get("error"):
        return jsonify({"error": f"LeetCode user '{leetcode_username}' not found. Check your username."}), 404

    result = {"github": github, "leetcode": leetcode}
    set_cached(cache_key, result)
    return jsonify(result)

@app.route("/api/digest")
def digest():
    github_username = request.args.get("github")
    leetcode_username = request.args.get("leetcode")

    if not github_username or not leetcode_username:
        return jsonify({"error": "Missing usernames"}), 400

    cache_key = f"digest:{github_username}:{leetcode_username}"
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)

    github = get_github_activity(github_username)
    leetcode = get_leetcode_activity(leetcode_username)
    text = generate_weekly_digest(github, leetcode)

    result = {"digest": text}
    set_cached(cache_key, result)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)