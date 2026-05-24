import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_leetcode_activity():
    username = os.getenv("LEETCODE_USERNAME")
    
    # LeetCode has a public GraphQL API — no auth needed
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
        print(f"Error: {response.status_code}")
        return {}
    
    data = response.json()
    user = data.get("data", {}).get("matchedUser")
    
    if not user:
        print(f"User {username} not found on LeetCode")
        return {}
    
    # parse submission stats
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


if __name__ == "__main__":
    activity = get_leetcode_activity()
    print(f"\nLeetCode Activity")
    print(f"================================")
    print(f"Username:      {activity['username']}")
    print(f"Total solved:  {activity['total_solved']}")
    print(f"Easy:          {activity['easy_solved']}")
    print(f"Medium:        {activity['medium_solved']}")
    print(f"Hard:          {activity['hard_solved']}")
    print(f"Current streak:{activity['streak']} days")
    print(f"Active days:   {activity['total_active_days']}")