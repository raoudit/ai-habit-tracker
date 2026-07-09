# 🧠 AI-Driven Multi-Modal Habit Tracker

An AI-powered personal growth dashboard combining fitness tracking, mood analysis, and habit intelligence using Python, NLP, and Data Science.

🔗 **Live Demo:**  
[AI Habit Tracker Demo](https://ai-habit-tracker-dxxtcwnwq5pn9cig2u6vot.streamlit.app/)
---

## 📌 Project Overview

A Self-Evolving Dashboard that tracks physical fitness, mental health, and intellectual growth using Python. The "Intelligence" lies in:
- **NLP Sentiment Analysis** on daily journal entries
- **Behavioral Correlation** between gym activity and mood
- **Streak Engine** that gamifies consistency
- **AI Coaching** that generates personalized suggestions

---

## 🧰 Technology Stack

| Layer | Tool |
|---|---|
| Language | Python 3.x |
| User Interface | Streamlit (reactive web dashboard) |
| Data Science | Pandas (time-series, CSV management) |
| AI / NLP | TextBlob / Lexicon-based Sentiment Analysis |
| Visualization | Plotly Express (interactive, zoomable graphs) |

---

## 📁 Project Structure


ai_habit_tracker/
├── app.py              ← Main Streamlit dashboard
├── sample_data.py      ← Demo data generator (30 days)
├── requirements.txt    ← Python dependencies
├── habit_data.csv      ← Auto-created local data store
└── README.md           ← This file

---

## 🌐 How To Use

1. Open the live AI Habit Tracker dashboard.

2. Enter your daily information:
   - Running distance
   - Gym activity
   - Sports activity
   - Reading progress
   - Daily journal entry

3. The system analyzes your inputs using:
   - NLP sentiment analysis
   - Habit tracking logic
   - Behavioral pattern analysis

4. Explore the dashboard:
   - View consistency streaks
   - Track fitness progress
   - Analyze mood trends
   - Receive personalized coaching suggestions

5. Use the insights to improve daily habits and maintain consistency.


---

## 🔍 Key Modules Explained

### 1. Input Module (Sidebar)
Captures multi-modal data:
- **Numerical**: Running km, Gym minutes, Book pages
- **Categorical**: Sport type (Football, Cricket, Yoga, etc.)
- **Textual**: Daily journal entry

### 2. Sentiment Analysis Engine

def analyze_sentiment(text: str) -> float:
    # Lexicon-based analysis
    # Returns polarity score: -1.0 (negative) to +1.0 (positive)

- Counts positive/negative keyword occurrences
- Normalizes by text length
- Returns polarity score + mood label

### 3. Streak & Motivation Engine

def calculate_streak(df: pd.DataFrame) -> int:
    # Compares today's date with last entry date
    # Consecutive days → streak increases
    # Break in days → streak resets


### 4. AI Coaching / Inference Engine

def generate_coaching_suggestion(entry, df) -> str:
    # Rule 1: Low gym + negative mood → Improvement Suggestion
    # Rule 2: High gym + negative mood → Recovery Alert
    # Rule 3: Good mood + low activity → Momentum Tip
    # Rule 4: Good reading + positive mood → Reinforcement
    # Rule 5: No journal → Journaling Reminder
    # Rule 6: Long streak → Celebration


---

## 📊 Dashboard Sections

| Section | Description |
|---|---|
| KPI Cards | Fire Streak, Total Entries, Avg Gym, Avg Mood |
| AI Coaching | Dynamic personalized suggestions |
| Physical Activity | Bar + Line combo chart (Gym + Running) |
| Mood Analysis | Sentiment area chart + Gym vs Mood scatter |
| Reading Progress | Daily bar chart + Cumulative line graph |
| Data Log | Full raw data table |

---

## ⚖️ Advantages & Disadvantages

### ✅ Advantages
- Holistic tracking: fitness, sports, reading, mental health in one view
- AI-generated coaching rather than just raw numbers
- Zero-cost infrastructure: local CSV + open-source libraries
- Streaks and daily motivation encourage long-term use

### ❌ Disadvantages
- Manual data entry (no smartwatch sync)
- Data stored locally (no multi-device sync)
- Basic NLP may misinterpret sarcasm or complex emotions

---

## 🚀 Future Scope

- **Predictive Analytics**: Scikit-Learn to predict habit relapse
- **Computer Vision**: OpenCV to track reading via book cover scanning
- **Cloud Sync**: Firebase / AWS for multi-device access
- **Smartwatch Integration**: Automatic data import from wearables

---

## 🎓 Academic Context

This project demonstrates how AI can be applied to **personal productivity** by:
1. Processing multi-modal user data (numerical + categorical + text)
2. Applying NLP for emotional state analysis
3. Identifying behavioral patterns through correlation
4. Gamifying discipline through a mathematical streak system
5. Generating data-driven motivational coaching

---

*Built with Python · Streamlit · Pandas · Plotly · NLP Sentiment Analysis*
