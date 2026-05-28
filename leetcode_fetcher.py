import requests
import json
from datetime import datetime, timezone, timedelta

def calculate_current_streak(submission_calendar: str) -> int:
    """Calculate current streak from submission calendar data."""
    if not submission_calendar:
        return 0
    
    try:
        calendar_data = json.loads(submission_calendar) if isinstance(submission_calendar, str) else submission_calendar
    except:
        return 0
    
    today = datetime.now(timezone.utc).date()
    streak = 0
    check_date = today
    
    while True:
        ts = str(int(datetime(check_date.year, check_date.month, check_date.day, tzinfo=timezone.utc).timestamp()))
        if ts in calendar_data and calendar_data[ts] > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            prev_date = check_date - timedelta(days=1)
            prev_ts = str(int(datetime(prev_date.year, prev_date.month, prev_date.day, tzinfo=timezone.utc).timestamp()))
            if streak == 0 and prev_ts in calendar_data and calendar_data[prev_ts] > 0:
                check_date = prev_date
            else:
                break
    
    return streak

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
            submissionCalendar
        }
        problemsSolvedBeatsStats {
            difficulty
            percentage
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
    print("Full calendar:", calendar)
    print("Full user keys:", user.keys())

    today = datetime.now(timezone.utc).date()
    today_ts = str(int(datetime(today.year, today.month, today.day, tzinfo=timezone.utc).timestamp()))
    calendar_data = json.loads(calendar.get("submissionCalendar", "{}"))
    submissions_today = calendar_data.get(today_ts, 0)

    return {
    "username": username,
    "total_solved": stats.get("All", 0),
    "easy_solved": stats.get("Easy", 0),
    "medium_solved": stats.get("Medium", 0),
    "hard_solved": stats.get("Hard", 0),
    "streak": calculate_current_streak(calendar.get("submissionCalendar", "{}")),
    "total_active_days": calendar.get("totalActiveDays", 0),
    "submissions_today": submissions_today
}

if __name__ == "__main__":
        result = get_leetcode_activity("adi0905")
        print(result)