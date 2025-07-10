import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Beach Volleyball League Tracker", page_icon="🏐")
st.title("🏐 Catholic Beach Volleyball League Tracker")

# === Load Google Sheet Data ===
conn = st.connection("gsheets", type="gspread")
df = conn.read(worksheet="Games", usecols=["Date", "Team 1", "Score 1", "Team 2", "Score 2"], ttl=5)

# === Clean + Sort ===
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# === Leaderboard Calculation ===
points = {}
for _, row in df.iterrows():
    points[row["Team 1"]] = points.get(row["Team 1"], 0) + row["Score 1"]
    points[row["Team 2"]] = points.get(row["Team 2"], 0) + row["Score 2"]
leaderboard = pd.DataFrame(points.items(), columns=["Team", "Points"]).sort_values("Points", ascending=False)

# === Match Input Form ===
st.subheader("➕ Log a New Match")
with st.form("log_match"):
    cols = st.columns(5)
    date = cols[0].date_input("Date", datetime.today())
    team1 = cols[1].text_input("Team 1")
    score1 = cols[2].number_input("Team 1 Score", min_value=0, value=0)
    team2 = cols[3].text_input("Team 2")
    score2 = cols[4].number_input("Team 2 Score", min_value=0, value=0)
    submitted = st.form_submit_button("Submit Match")

    if submitted:
        new_match = pd.DataFrame.from_records([{
            "Date": date.strftime("%Y-%m-%d"),
            "Team 1": team1,
            "Score 1": score1,
            "Team 2": team2,
            "Score 2": score2
        }])
        updated = pd.concat([df, new_match], ignore_index=True)
        conn.update(worksheet="Games", data=updated)
        st.success("Match logged!")
        st.rerun()

# === Display Match History and Leaderboard ===
st.subheader("📋 Match History")
st.dataframe(df, use_container_width=True)

st.subheader("🏆 Leaderboard")
st.table(leaderboard)