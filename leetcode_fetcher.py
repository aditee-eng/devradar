import requests

def get_leetcode_activity(username: str) -> dict:
    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            userCalendar {
                streak
                totalActiveDays
            }
        }
    }
    """

    response = requests.post(
        url,
        json={"query": query, "variables": {"username": username}},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        return {"username": username, "total_solved": 0, "easy_solved": 0, "medium_solved": 0, "hard_solved": 0, "streak": 0, "total_active_days": 0}

    data = response.json()
    user = data.get("data", {}).get("matchedUser")

    if not user:
      return {"error": "user_not_found"}
    stats = {}
    for item in user.get("submitStats", {}).get("acSubmissionNum", []):
        stats[item["difficulty"]] = item["count"]

    calendar = user.get("userCalendar", {})

    return {
        "username": username,
        "total_solved": stats.get("All", 0),
        "easy_solved": stats.get("Easy", 0),
        "medium_solved": stats.get("Medium", 0),
        "hard_solved": stats.get("Hard", 0),
        "streak": calendar.get("streak", 0),
        "total_active_days": calendar.get("totalActiveDays", 0)
    }