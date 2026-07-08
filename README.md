# 🧠 AI-Driven Multi-Modal Habit Tracker

> **Python Lab Project** | AI + Data Science + NLP + Interactive Dashboard

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

```
ai_habit_tracker/
├── app.py              ← Main Streamlit dashboard
├── sample_data.py      ← Demo data generator (30 days)
├── requirements.txt    ← Python dependencies
├── habit_data.csv      ← Auto-created local data store
└── README.md           ← This file
```

---

## ▶️ How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — (Optional) Generate sample data
```bash
python sample_data.py
```

### Step 3 — Launch the app
```bash
streamlit run app.py
```

The dashboard opens automatically in your browser at `http://localhost:8501`

---

## 🔍 Key Modules Explained

### 1. Input Module (Sidebar)
Captures multi-modal data:
- **Numerical**: Running km, Gym minutes, Book pages
- **Categorical**: Sport type (Football, Cricket, Yoga, etc.)
- **Textual**: Daily journal entry

### 2. Sentiment Analysis Engine
```python
def analyze_sentiment(text: str) -> float:
    # Lexicon-based analysis
    # Returns polarity score: -1.0 (negative) to +1.0 (positive)
```
- Counts positive/negative keyword occurrences
- Normalizes by text length
- Returns polarity score + mood label

### 3. Streak & Motivation Engine
```python
def calculate_streak(df: pd.DataFrame) -> int:
    # Compares today's date with last entry date
    # Consecutive days → streak increases
    # Break in days → streak resets
```

### 4. AI Coaching / Inference Engine
```python
def generate_coaching_suggestion(entry, df) -> str:
    # Rule 1: Low gym + negative mood → Improvement Suggestion
    # Rule 2: High gym + negative mood → Recovery Alert
    # Rule 3: Good mood + low activity → Momentum Tip
    # Rule 4: Good reading + positive mood → Reinforcement
    # Rule 5: No journal → Journaling Reminder
    # Rule 6: Long streak → Celebration
```

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
