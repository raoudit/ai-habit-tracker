"""
sample_data.py — Generate sample habit data for demo/testing purposes.
Run this file to pre-populate habit_data.csv with 30 days of realistic data.

Usage:
    python sample_data.py
"""

import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

SPORTS = ["None", "Football", "Basketball", "Cricket", "Yoga", "None", "Cycling"]

JOURNAL_ENTRIES = [
    "Felt really energetic and productive today. Had a great workout!",
    "Tired after work but managed to read a bit. Feeling okay.",
    "Stressed about deadlines. Skipped gym, not happy about it.",
    "Amazing run in the morning! Mood is fantastic.",
    "Lazy day, didn't do much. Feeling a bit down.",
    "Very motivated today! Crushed my workout and read 40 pages.",
    "Feeling overwhelmed. Work is stressful and I'm exhausted.",
    "Had a wonderful time playing cricket with friends. Happy!",
    "Neutral day. Nothing special, just regular routine.",
    "Excellent focus today! Finished a whole chapter.",
    "Anxious about exams. Hard to focus on anything.",
    "Feeling strong and accomplished after a tough gym session.",
    "Good day overall. Ran 5km and feeling refreshed.",
    "Bit bored and unmotivated. Hope tomorrow is better.",
    "Great mood! Positive vibes all around today.",
]

records = []
today = date.today()

for i in range(30, 0, -1):
    entry_date = today - timedelta(days=i)
    journal = random.choice(JOURNAL_ENTRIES)

    # Simple keyword-based sentiment
    pos_words = {"great","amazing","fantastic","wonderful","strong","excellent",
                 "happy","productive","energetic","motivated","positive","refreshed","accomplished"}
    neg_words = {"sad","tired","stressed","overwhelmed","anxious","bored","down",
                 "exhausted","unmotivated","frustrated","lazy"}
    words = set(journal.lower().split())
    pos = len(words & pos_words)
    neg = len(words & neg_words)
    raw = (pos - neg) / max(len(journal.split()), 1) * 5
    score = round(max(-1.0, min(1.0, raw)), 4)

    if score >= 0.5:   mood = "😊 Very Positive"
    elif score >= 0.1: mood = "🙂 Positive"
    elif score >= -0.1:mood = "😐 Neutral"
    elif score >= -0.5:mood = "😕 Negative"
    else:              mood = "😞 Very Negative"

    records.append({
        "date": str(entry_date),
        "running_km": round(random.uniform(0, 8), 1) if random.random() > 0.4 else 0,
        "gym_minutes": random.choice([0, 0, 30, 45, 60, 75, 90]) if random.random() > 0.3 else 0,
        "sport": random.choice(SPORTS),
        "book_pages": random.randint(0, 60) if random.random() > 0.3 else 0,
        "journal": journal,
        "sentiment_score": score,
        "mood_label": mood,
    })

df = pd.DataFrame(records)
df.to_csv("habit_data.csv", index=False)
print(f"✅ Sample data generated: {len(df)} entries saved to habit_data.csv")
print(df[["date", "gym_minutes", "running_km", "book_pages", "mood_label"]].tail(7).to_string(index=False))
