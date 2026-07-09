"""
AI-Driven Multi-Modal Habit Tracker  ✦ Enhanced Edition
=========================================================
New Features Added:
  1. Weekly PDF Report Generator (downloadable)
  2. Habit Relapse Predictor with Gauge Chart
  3. Sleep & Water / Nutrition Logging + Charts
  4. Goal Setting & Weekly Progress Bars
  5. Activity Heatmap Calendar (GitHub-style)
  6. Wellness Radar / Spider Chart (5 dimensions)
  7. Trendline on Gym vs Mood scatter
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os


POSITIVE_WORDS = {
    "happy","great","amazing","good","excellent","wonderful","fantastic",
    "productive","energetic","motivated","excited","awesome","positive",
    "strong","focused","refreshed","accomplished","proud","joyful","calm",
    "confident","peaceful","inspired","cheerful","optimistic","grateful"
}
NEGATIVE_WORDS = {
    "sad","bad","terrible","awful","tired","exhausted","lazy","stressed",
    "depressed","anxious","worried","angry","frustrated","sick","unhappy",
    "unmotivated","bored","lonely","overwhelmed","hopeless","miserable",
    "irritated","gloomy","nervous","drained","weak","upset"
}

def analyze_sentiment(text: str) -> float:
    if not text or not text.strip():
        return 0.0
    words = text.lower().split()
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = len(words)
    if total == 0:
        return 0.0
    return max(-1.0, min(1.0, (pos - neg) / total * 5))

def get_mood_label(p: float) -> str:
    if p >= 0.5:    return "😊 Very Positive"
    elif p >= 0.1:  return "🙂 Positive"
    elif p >= -0.1: return "😐 Neutral"
    elif p >= -0.5: return "😕 Negative"
    else:           return "😞 Very Negative"



#  STREAK ENGINE

def calculate_streak(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    sorted_dates = sorted(df["date"].dt.date.unique(), reverse=True)
    today = date.today()
    streak = 0
    expected = today
    for d in sorted_dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d < expected:
            break
    return streak



# HABIT RELAPSE PREDICTOR

def predict_relapse_risk(df: pd.DataFrame) -> dict:
    if len(df) < 3:
        return {"score": 0, "level": "Insufficient Data", "color": "#94a3b8", "tips": ["Log at least 3 days to enable prediction."]}

    recent = df.tail(7).copy()
    prev   = df.tail(14).head(7).copy() if len(df) >= 14 else recent.copy()
    score  = 0

    r_gym = pd.to_numeric(recent["gym_minutes"], errors="coerce").mean()
    p_gym = pd.to_numeric(prev["gym_minutes"],   errors="coerce").mean()
    if p_gym > 0 and r_gym < p_gym * 0.5:
        score += 30

    recent_moods = pd.to_numeric(recent["sentiment_score"], errors="coerce").fillna(0)
    score += int((recent_moods < -0.1).sum()) * 7

    if len(recent) < 5:
        score += (7 - len(recent)) * 5

    if "sleep_hours" in recent.columns:
        avg_sleep = pd.to_numeric(recent["sleep_hours"], errors="coerce").mean()
        if avg_sleep < 6:
            score += 20
        elif avg_sleep < 7:
            score += 10

    score = min(100, score)

    if score >= 70:
        level, color = "🔴 HIGH RISK", "#ef4444"
        tips = [
            "Activity dropped sharply — start with just 10 minutes of movement.",
            "Mood has been consistently low. Try journaling or calling a friend.",
            "Set a smaller, easier daily goal to rebuild momentum."
        ]
    elif score >= 40:
        level, color = "🟡 MODERATE RISK", "#f59e0b"
        tips = [
            "Early signs of habit decay. Don't break the chain!",
            "Try habit stacking — attach your habit to something you already do daily."
        ]
    else:
        level, color = "🟢 LOW RISK", "#22c55e"
        tips = ["Great consistency! Maintain your current routine."]

    return {"score": score, "level": level, "color": color, "tips": tips}



#  WELLNESS SCORE  (5-dimensional, 0–100)

def calculate_wellness_score(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total": 0, "fitness": 0, "mental": 0, "sleep": 0, "reading": 0, "consistency": 0}

    recent = df.tail(7).copy()
    gym    = pd.to_numeric(recent["gym_minutes"],    errors="coerce").mean() or 0
    run    = pd.to_numeric(recent["running_km"],     errors="coerce").mean() or 0
    mood   = pd.to_numeric(recent["sentiment_score"],errors="coerce").mean() or 0
    pages  = pd.to_numeric(recent["book_pages"],     errors="coerce").mean() or 0
    sleep  = pd.to_numeric(recent.get("sleep_hours", pd.Series([7]*len(recent))), errors="coerce").mean() or 7

    fitness     = min(100, (gym / 60) * 50 + (run / 5) * 50)
    mental      = min(100, ((mood + 1) / 2) * 100)
    sleep_score = min(100, max(0, (sleep - 4) / 4 * 100))
    reading     = min(100, (pages / 30) * 100)
    consistency = min(100, calculate_streak(df) * 10)

    total = round(fitness*0.25 + mental*0.25 + sleep_score*0.20 + reading*0.15 + consistency*0.15, 1)

    return {
        "total":       total,
        "fitness":     round(fitness,     1),
        "mental":      round(mental,      1),
        "sleep":       round(sleep_score, 1),
        "reading":     round(reading,     1),
        "consistency": round(consistency, 1)
    }



# ⑤ AI COACHING ENGINE

def generate_coaching(entry: dict, df: pd.DataFrame) -> list:
    score  = entry.get("sentiment_score", 0)
    gym    = entry.get("gym_minutes", 0) or 0
    pages  = entry.get("book_pages",  0) or 0
    sleep  = entry.get("sleep_hours", 7) or 7
    streak = calculate_streak(df)
    msgs   = []

    if gym < 20 and score < -0.1:
        msgs.append(("⚠️ Improvement Suggestion",
            "Your mood is low and activity is minimal. Even a 15-minute walk raises serotonin. Start small!",
            "#f97316"))
    elif gym >= 60 and score < -0.1:
        msgs.append(("💤 Recovery Alert",
            "You trained hard but still feel down. Overtraining can affect mental health — prioritize rest.",
            "#8b5cf6"))
    elif score > 0.2 and gym < 20:
        msgs.append(("🏃 Capitalize Your Energy",
            "You feel great today! Perfect time to work out — positive mood + movement = maximum benefit.",
            "#3b82f6"))

    if sleep < 6:
        msgs.append(("🛏️ Sleep Deficit Detected",
            f"Only {sleep}h of sleep. Under 6 hours impairs memory, mood, and physical performance significantly.",
            "#ef4444"))
    elif sleep >= 8:
        msgs.append(("✨ Sleep Champion",
            "Excellent sleep! You're giving your brain and body the recovery it needs.",
            "#22c55e"))

    if pages > 20 and score > 0.1:
        msgs.append(("📚 Intellectual Momentum",
            "Reading + positive mood creates a powerful cognitive growth loop. You are in the zone!",
            "#06b6d4"))

    if streak >= 7:
        msgs.append(("🔥 Streak Master",
            f"{streak}-day streak! You're in the top tier of consistent habit trackers. Keep going!",
            "#f59e0b"))
    elif streak == 0:
        msgs.append(("🌱 Fresh Start",
            "Every champion was once a beginner. Log in tomorrow to start your streak!",
            "#64748b"))

    if not entry.get("journal", "").strip():
        msgs.append(("📝 Journal Reminder",
            "Journaling just 5 minutes/day improves emotional regulation significantly. Try it tomorrow!",
            "#a855f7"))

    if not msgs:
        msgs.append(("✅ On Track",
            "You are building excellent habits. Consistency is the compound interest of self-improvement.",
            "#22c55e"))
    return msgs



#  DATA MANAGER (CSV local storage)

DATA_FILE = "habit_data.csv"
COLUMNS   = ["date","running_km","gym_minutes","sport","book_pages",
              "sleep_hours","water_glasses","journal","sentiment_score","mood_label"]

def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = 0 if col not in ["sport","journal","mood_label"] else ""
        return df
    return pd.DataFrame(columns=COLUMNS)

def save_entry(entry: dict):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)



#  WEEKLY REPORT GENERATOR (downloadable .txt)

def generate_weekly_report(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data available for report."

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    week_df = df[df["date"] >= pd.Timestamp(date.today() - timedelta(days=7))]
    if week_df.empty:
        week_df = df.tail(7)

    streak = calculate_streak(df)
    ws     = calculate_wellness_score(df)
    risk   = predict_relapse_risk(df)

    avg_gym  = round(pd.to_numeric(week_df["gym_minutes"],      errors="coerce").mean(), 1)
    avg_run  = round(pd.to_numeric(week_df["running_km"],       errors="coerce").mean(), 1)
    avg_mood = round(pd.to_numeric(week_df["sentiment_score"],  errors="coerce").mean(), 2)
    avg_pgs  = round(pd.to_numeric(week_df["book_pages"],       errors="coerce").mean(), 1)
    avg_slp  = round(pd.to_numeric(week_df.get("sleep_hours",   pd.Series([0]*len(week_df))), errors="coerce").mean(), 1)
    total_pg = int(pd.to_numeric(week_df["book_pages"],         errors="coerce").sum())

    report = f"""
╔══════════════════════════════════════════════════════╗
║       AI HABIT TRACKER — WEEKLY PROGRESS REPORT      ║
║       Generated : {date.today().strftime('%B %d, %Y')}                    ║
╚══════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OVERALL WELLNESS SCORE  :  {ws['total']} / 100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔥 Current Streak       : {streak} days
  ⚠️  Relapse Risk         : {risk['level']}  ({risk['score']}/100)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WEEKLY AVERAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💪 Gym              : {avg_gym} min/day
  🏃 Running          : {avg_run} km/day
  😊 Mood Score       : {avg_mood}  (scale: -1.0 to +1.0)
  📚 Pages / Day      : {avg_pgs}   (Total this week: {total_pg} pages)
  🛏️  Sleep            : {avg_slp} hrs/night

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WELLNESS DIMENSION BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Fitness Score       : {ws['fitness']} / 100
  Mental Score        : {ws['mental']} / 100
  Sleep Score         : {ws['sleep']} / 100
  Reading Score       : {ws['reading']} / 100
  Consistency Score   : {ws['consistency']} / 100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI PERSONALIZED RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for tip in risk["tips"]:
        report += f"  • {tip}\n"

    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI Habit Tracker | Python Lab Project
  Stack: Python · Streamlit · Pandas · Plotly · NLP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report



#  HEATMAP PREP

def build_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["activity_score"] = (
        pd.to_numeric(df["gym_minutes"], errors="coerce").fillna(0).clip(0,90)/90*50 +
        pd.to_numeric(df["running_km"],  errors="coerce").fillna(0).clip(0,10)/10*30 +
        pd.to_numeric(df["book_pages"],  errors="coerce").fillna(0).clip(0,50)/50*20
    ).round(1)
    df["week"]    = df["date"].dt.isocalendar().week.astype(int)
    df["weekday"] = df["date"].dt.weekday
    df["date_str"]= df["date"].dt.strftime("%b %d")
    return df



#  STREAMLIT MAIN

def main():
    st.set_page_config(
        page_title="AI Habit Tracker",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .kpi-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border-radius: 14px; padding: 18px; text-align: center;
        border: 1px solid #4338ca; color: white;
    }
    .kpi-val  { font-size: 2rem; font-weight: 800; color: #a5b4fc; }
    .kpi-lbl  { font-size: 0.8rem; color: #c7d2fe; margin-top: 4px; }
    .coach-card {
        border-radius: 10px; padding: 14px 18px;
        border-left: 4px solid; margin-bottom: 10px;
        background: rgba(255,255,255,0.03);
    }
    .section-hdr {
        font-size: 1.15rem; font-weight: 700; color: #818cf8;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px; margin: 16px 0 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🧠 AI-Driven Multi-Modal Habit Tracker</div>', unsafe_allow_html=True)
    st.caption("Track fitness · mental health · sleep · nutrition · reading — powered by AI insights")
    st.markdown("---")

    df     = load_data()
    streak = calculate_streak(df)

    #  SIDEBAR
    with st.sidebar:
        st.markdown("### 📥 Log Today's Habits")
        st.caption(f"📅 {date.today().strftime('%A, %B %d %Y')}")
        st.markdown("---")

        st.markdown("**🏃 Physical Fitness**")
        running_km  = st.number_input("Running (km)",        min_value=0.0, step=0.5, value=0.0)
        gym_minutes = st.number_input("Gym / Workout (min)", min_value=0,   step=5,   value=0)
        sport = st.selectbox("Recreational Sport", [
            "None","Football","Basketball","Cricket","Tennis",
            "Swimming","Cycling","Badminton","Yoga","Other"
        ])
        st.markdown("---")

        st.markdown("**📚 Intellectual Growth**")
        book_pages = st.number_input("Book Pages Read", min_value=0, step=1, value=0)
        st.markdown("---")

        st.markdown("**🛏️ Sleep & 💧 Hydration**")
        sleep_hours   = st.slider("Sleep (hours)",   0.0, 12.0, 7.0, 0.5)
        water_glasses = st.slider("Water (glasses)", 0,   15,   8,   1)
        st.markdown("---")

        st.markdown("**📝 Daily Journal**")
        journal_text = st.text_area(
            "How are you feeling today?",
            placeholder="Describe your day, energy levels, emotions...",
            height=110
        )
        st.markdown("---")

        with st.expander("🎯 Set Weekly Goals"):
            g_gym  = st.number_input("Gym target (min/week)",  value=st.session_state.get("g_gym",  300), step=30)
            g_run  = st.number_input("Running target (km/week)",value=st.session_state.get("g_run",  20.0),step=1.0)
            g_read = st.number_input("Reading target (pages/week)",value=st.session_state.get("g_read",100),step=10)
            if st.button("💾 Save Goals"):
                st.session_state["g_gym"]  = g_gym
                st.session_state["g_run"]  = g_run
                st.session_state["g_read"] = g_read
                st.success("Goals saved!")

        if st.button("✅ Save Today's Entry", use_container_width=True, type="primary"):
            sentiment = analyze_sentiment(journal_text)
            entry = {
                "date": str(date.today()),
                "running_km": running_km, "gym_minutes": gym_minutes,
                "sport": sport, "book_pages": book_pages,
                "sleep_hours": sleep_hours, "water_glasses": water_glasses,
                "journal": journal_text,
                "sentiment_score": round(sentiment, 4),
                "mood_label": get_mood_label(sentiment)
            }
            save_entry(entry)
            df     = load_data()
            streak = calculate_streak(df)
            st.success("✅ Entry saved!")
            st.session_state["last_entry"] = entry
            st.session_state["coaching"]   = generate_coaching(entry, df)

    # ─── KPI ROW ───────────────────────────────────────
    ws   = calculate_wellness_score(df)
    risk = predict_relapse_risk(df)

    c1,c2,c3,c4,c5 = st.columns(5)
    avg_gym_7 = round(pd.to_numeric(df["gym_minutes"], errors="coerce").tail(7).mean(), 0) if not df.empty else 0
    avg_mood_7= round(pd.to_numeric(df["sentiment_score"],errors="coerce").tail(7).mean(), 2) if not df.empty else 0

    for col, icon, val, lbl in zip(
        [c1,c2,c3,c4,c5],
        ["🔥","⭐","💪","😊","📅"],
        [f"{streak}", f"{ws['total']}", f"{avg_gym_7:.0f} min", f"{avg_mood_7:.2f}", f"{len(df)}"],
        ["Day Streak","Wellness Score","Avg Gym/Day","Avg Mood Score","Total Entries"]
    ):
        col.markdown(f"""
        <div class="kpi-box">
            <div style="font-size:1.6rem">{icon}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GOAL PROGRESS BARS 
    if not df.empty:
        df_temp = df.copy()
        df_temp["date"] = pd.to_datetime(df_temp["date"])
        wk = df_temp[df_temp["date"] >= pd.Timestamp(date.today() - timedelta(days=7))]

        g_gym  = st.session_state.get("g_gym",  300)
        g_run  = st.session_state.get("g_run",  20.0)
        g_read = st.session_state.get("g_read", 100)

        w_gym  = int(pd.to_numeric(wk["gym_minutes"], errors="coerce").sum())
        w_run  = round(pd.to_numeric(wk["running_km"], errors="coerce").sum(), 1)
        w_read = int(pd.to_numeric(wk["book_pages"],   errors="coerce").sum())

        st.markdown('<div class="section-hdr">🎯 Weekly Goal Progress</div>', unsafe_allow_html=True)
        p1,p2,p3 = st.columns(3)
        with p1:
            st.caption(f"💪 Gym:  **{w_gym} / {g_gym} min**")
            st.progress(min(1.0, w_gym / max(g_gym, 1)))
        with p2:
            st.caption(f"🏃 Run:  **{w_run} / {g_run} km**")
            st.progress(min(1.0, w_run / max(g_run, 1)))
        with p3:
            st.caption(f"📚 Read: **{w_read} / {g_read} pages**")
            st.progress(min(1.0, w_read / max(g_read, 1)))

    st.markdown("---")

    #  RELAPSE PREDICTOR + RADAR
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-hdr">⚠️ Habit Relapse Predictor (AI)</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="border-radius:12px; padding:14px 18px; border-left:5px solid {risk['color']};
                    background:rgba(0,0,0,0.15); margin-bottom:10px">
            <b style="font-size:1.1rem">{risk['level']}</b><br>
            <span style="color:#94a3b8;font-size:0.85rem">Risk Score: {risk['score']} / 100</span>
        </div>""", unsafe_allow_html=True)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk["score"],
            domain={"x":[0,1],"y":[0,1]},
            title={"text":"Relapse Risk %","font":{"color":"white"}},
            number={"font":{"color":"white"}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":"white"},
                "bar":{"color":risk["color"]},
                "steps":[
                    {"range":[0,40],  "color":"#1a2e1a"},
                    {"range":[40,70], "color":"#2e2a1a"},
                    {"range":[70,100],"color":"#2e1a1a"},
                ],
                "threshold":{"line":{"color":"white","width":3},"thickness":0.75,"value":risk["score"]}
            }
        ))
        gauge.update_layout(height=260, margin=dict(t=40,b=10,l=20,r=20),
                             paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(gauge, use_container_width=True)
        for tip in risk["tips"]:
            st.markdown(f"• {tip}")

    with right:
        st.markdown('<div class="section-hdr">🕸️ Wellness Radar Chart (5 Dimensions)</div>', unsafe_allow_html=True)
        cats = ["Fitness","Mental Health","Sleep","Reading","Consistency"]
        vals = [ws["fitness"],ws["mental"],ws["sleep"],ws["reading"],ws["consistency"]]
        radar = go.Figure(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]],
            fill="toself",
            fillcolor="rgba(99,102,241,0.25)",
            line=dict(color="#6366f1",width=2),
            marker=dict(color="#818cf8",size=7)
        ))
        radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True,range=[0,100],gridcolor="#334155",color="#64748b"),
                angularaxis=dict(gridcolor="#334155",color="#94a3b8")
            ),
            paper_bgcolor="rgba(0,0,0,0)", font_color="white",
            height=340, margin=dict(t=30,b=10)
        )
        st.plotly_chart(radar, use_container_width=True)

    st.markdown("---")

    #  AI COACHING 
    if "coaching" in st.session_state:
        st.markdown('<div class="section-hdr">🤖 AI Coaching Insights</div>', unsafe_allow_html=True)
        for title, msg, color in st.session_state["coaching"]:
            st.markdown(f"""
            <div class="coach-card" style="border-color:{color}">
                <b style="color:{color}">{title}</b><br>
                <span style="color:#cbd5e1;font-size:0.9rem">{msg}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("---")

    #  CHARTS 
    if not df.empty:
        dfp = df.copy()
        dfp["date"] = pd.to_datetime(dfp["date"])
        dfp = dfp.sort_values("date")
        for col in ["gym_minutes","running_km","book_pages","sentiment_score","sleep_hours","water_glasses"]:
            dfp[col] = pd.to_numeric(dfp[col], errors="coerce").fillna(0)

        BG = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                  font_color="white",
                  xaxis=dict(gridcolor="#1e293b"),
                  height=380)

        t1,t2,t3,t4,t5 = st.tabs([
            "📊 Physical Activity",
            "😊 Mood & Mental Health",
            "📚 Reading Progress",
            "🛏️ Sleep & Hydration",
            "🗓️ Activity Heatmap"
        ])

        with t1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=dfp["date"], y=dfp["gym_minutes"],
                                  name="Gym (min)", marker_color="#6366f1", opacity=0.85))
            fig.add_trace(go.Scatter(x=dfp["date"], y=dfp["running_km"],
                                      name="Running (km)", yaxis="y2",
                                      line=dict(color="#10b981",width=2.5),
                                      mode="lines+markers", marker=dict(size=6)))
            fig.update_layout(**BG, title="Gym Minutes & Running Over Time",
                               yaxis=dict(title="Gym (min)",gridcolor="#1e293b"),
                               yaxis2=dict(title="Running (km)",overlaying="y",side="right",
                                           gridcolor="#1e293b",color="#10b981"),
                               legend=dict(orientation="h",y=1.1))
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            fig2 = px.area(dfp, x="date", y="sentiment_score",
                            title="Daily Mood Polarity Score (NLP Sentiment)",
                            color_discrete_sequence=["#f59e0b"])
            fig2.add_hline(y=0, line_dash="dash", line_color="#64748b",
                            annotation_text="Neutral", annotation_font_color="#94a3b8")
            fig2.update_layout(**BG, yaxis=dict(gridcolor="#1e293b"))
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("#### 🔬 Behavioral Correlation: Gym vs Mood")
            fig3 = px.scatter(dfp, x="gym_minutes", y="sentiment_score",
                               color="sentiment_score", color_continuous_scale="RdYlGn",
                               trendline="ols", opacity=0.85,
                               title="Does Exercise Improve Mood? (Trendline = ML Regression)",
                               labels={"gym_minutes":"Gym (min)","sentiment_score":"Mood Score"})
            fig3.update_layout(**BG, yaxis=dict(gridcolor="#1e293b"))
            st.plotly_chart(fig3, use_container_width=True)

        with t3:
            fig4 = px.bar(dfp, x="date", y="book_pages",
                           color="book_pages", color_continuous_scale="Blues",
                           title="Daily Pages Read")
            fig4.update_layout(**BG, yaxis=dict(gridcolor="#1e293b"))
            st.plotly_chart(fig4, use_container_width=True)

            dfp["cumulative_pages"] = dfp["book_pages"].cumsum()
            fig5 = px.line(dfp, x="date", y="cumulative_pages",
                            title="Cumulative Reading Progress",
                            labels={"cumulative_pages":"Total Pages"})
            fig5.update_traces(line_color="#8b5cf6", fill="tozeroy",
                                fillcolor="rgba(139,92,246,0.15)")
            fig5.update_layout(**BG, yaxis=dict(gridcolor="#1e293b"))
            st.plotly_chart(fig5, use_container_width=True)

        with t4:
            fig6 = go.Figure()
            fig6.add_trace(go.Scatter(
                x=dfp["date"], y=dfp["sleep_hours"], name="Sleep (hrs)",
                fill="tozeroy", fillcolor="rgba(99,102,241,0.2)",
                line=dict(color="#6366f1",width=2.5)
            ))
            fig6.add_hline(y=8, line_dash="dot", line_color="#22c55e",
                            annotation_text="Optimal 8h", annotation_font_color="#22c55e")
            fig6.add_hline(y=6, line_dash="dot", line_color="#ef4444",
                            annotation_text="Min 6h", annotation_font_color="#ef4444")
            fig6.update_layout(**BG, title="Sleep Hours Trend",
                                yaxis=dict(title="Hours",range=[0,12],gridcolor="#1e293b"))
            st.plotly_chart(fig6, use_container_width=True)

            fig7 = px.bar(dfp, x="date", y="water_glasses",
                           title="Daily Water Intake (glasses)",
                           color="water_glasses", color_continuous_scale="Blues")
            fig7.add_hline(y=8, line_dash="dash", line_color="#38bdf8",
                            annotation_text="Recommended 8 glasses")
            fig7.update_layout(**BG, yaxis=dict(gridcolor="#1e293b"))
            st.plotly_chart(fig7, use_container_width=True)

        with t5:
            st.markdown("#### 🗓️ GitHub-Style Activity Heatmap")
            hm = build_heatmap_data(df)
            if not hm.empty:
                pivot = hm.pivot_table(
                    index="weekday", columns="week",
                    values="activity_score", aggfunc="mean"
                ).fillna(0)
                day_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                fig8 = px.imshow(
                    pivot,
                    labels=dict(x="Week of Year", y="Day", color="Activity Score"),
                    y=[day_labels[i] for i in pivot.index],
                    color_continuous_scale="Viridis",
                    title="Activity Heatmap — Gym 50% + Running 30% + Reading 20%"
                )
                fig8.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(0,0,0,0)",
                                    font_color="white", height=320)
                st.plotly_chart(fig8, use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-hdr">📋 Complete Habit Data Log</div>', unsafe_allow_html=True)
        disp = dfp.copy()
        disp["date"] = disp["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(
            disp[["date","running_km","gym_minutes","sport","book_pages",
                  "sleep_hours","water_glasses","sentiment_score","mood_label"]],
            use_container_width=True, hide_index=True
        )
    else:
        st.info("👈 No data yet! Use the sidebar to log your first habit entry.")

    #  WEEKLY REPORT DOWNLOAD
    st.markdown("---")
    st.markdown('<div class="section-hdr">📄 Weekly Progress Report</div>', unsafe_allow_html=True)
    report_text = generate_weekly_report(df)
    r1, r2 = st.columns([2, 1])
    with r1:
        st.text(report_text)
    with r2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Report (.txt)",
            data=report_text,
            file_name=f"habit_report_{date.today()}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("🧠 AI Habit Tracker — Enhanced Edition  |  Python · Streamlit · Pandas · Plotly · NLP Sentiment Analysis")


if __name__ == "__main__":
    main()
