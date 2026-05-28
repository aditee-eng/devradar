import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = "devradar.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            captured_at TEXT NOT NULL,
            commits_this_week INTEGER,
            prs_opened INTEGER,
            repo_count INTEGER,
            repos_active TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leetcode_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            captured_at TEXT NOT NULL,
            total_solved INTEGER,
            easy_solved INTEGER,
            medium_solved INTEGER,
            hard_solved INTEGER,
            streak INTEGER,
            total_active_days INTEGER
        )
    """)

    conn.commit()
    conn.close()

def save_github_snapshot(username: str, data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO github_snapshots 
        (username, captured_at, commits_this_week, prs_opened, repo_count, repos_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        datetime.now(timezone.utc).isoformat(),
        data.get("commits_this_week", 0),
        data.get("prs_opened", 0),
        data.get("repo_count", 0),
        ", ".join(data.get("repos_active", []))
    ))
    conn.commit()
    conn.close()

def save_leetcode_snapshot(username: str, data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leetcode_snapshots
        (username, captured_at, total_solved, easy_solved, medium_solved, hard_solved, streak, total_active_days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        datetime.now(timezone.utc).isoformat(),
        data.get("total_solved", 0),
        data.get("easy_solved", 0),
        data.get("medium_solved", 0),
        data.get("hard_solved", 0),
        data.get("streak", 0),
        data.get("total_active_days", 0)
    ))
    conn.commit()
    conn.close()

def get_github_history(username: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT captured_at, commits_this_week, prs_opened, repo_count
        FROM github_snapshots
        WHERE username = ?
        ORDER BY captured_at DESC
        LIMIT 8
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_leetcode_history(username: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT captured_at, total_solved, easy_solved, medium_solved, hard_solved, streak
        FROM leetcode_snapshots
        WHERE username = ?
        ORDER BY captured_at DESC
        LIMIT 8
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows