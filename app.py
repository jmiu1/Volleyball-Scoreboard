import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Beach Volleyball League Tracker", page_icon="🏐")
st.title("🏐 Catholic Beach Volleyball League Tracker")

# === Load Credentials from secrets.toml ===
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"], scopes=scope
)

gc = gspread.authorize(credentials)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Sij1rPlC4WGGP37S38DTm2lFpaSd-3_ldsY2ABf663s")
worksheet = sh.worksheet("Games")
data = worksheet.get_all_records()

game_data_df = pd.DataFrame(data)

# === Clean + Sort ===
game_data_df["Date"] = pd.to_datetime(game_data_df["Date"])
game_data_df = game_data_df.sort_values("Date")

# === Leaderboard Calculation ===
points = {}
for _, row in game_data_df.iterrows():
    points[row["Team 1"]] = points.get(row["Team 1"], 0) + row["Score 1"]
    points[row["Team 2"]] = points.get(row["Team 2"], 0) + row["Score 2"]
leaderboard_df = pd.DataFrame(points.items(), columns=["Team", "Points"]).sort_values("Points", ascending=False)

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
        updated = pd.concat([game_data_df, new_match], ignore_index=True)

        # Clear and update worksheet with new data
        worksheet.clear()
        worksheet.update([updated.columns.values.tolist()] + updated.values.tolist())

        st.success("Match logged!")
        st.rerun()

# === Display Match History and Leaderboard ===
st.subheader("📋 Match History")
st.dataframe(game_data_df.style.hide_index(), use_container_width=True)

st.subheader("🏆 Leaderboard")
st.table(leaderboard_df.style.hide_index())
