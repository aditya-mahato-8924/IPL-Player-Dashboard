import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# setting the configuration of the page
st.set_page_config(
    page_title="Virat Kohli IPL Dashboard",
    page_icon= "🏏",
    initial_sidebar_state="auto")

# load the data
balls = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")
matches = pd.read_csv("IPL_Matches_2008_2022.csv")

st.header("Virat Kohli IPL Analysis", divider=True)


# sidebar
selected_section = st.sidebar.selectbox("Select Analysis Section",
                     ["Batting Analysis", "Bowling Analysis", "Fielding Analysis"])

st.image("image.png", caption="Virat Kohli", use_container_width=True)

st.divider()

# Personal Info. Section

st.subheader("Personal Info.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Age")
    st.metric(
        label=str(36),
        value="",
        border=True
    )

    st.markdown("#### Nationality")
    st.metric(
        label="Indian",
        value="",
        border=True
    )

    st.markdown("#### Teams Played")
    st.metric(
        label="Royal Challengers Bangalore",
        value="",
        border=True
    )


with col2:
    st.markdown("#### Debut Year")
    st.metric(
        label="2008",
        value="",
        border=True
    )

    st.markdown("#### Primary Role")
    st.metric(
        label="Top-order Batsman",
        value="",
        border=True
    )

with col3:
    st.markdown("#### Batting Style")
    st.metric(
        label="Right-hand bat",
        value="",
        border=True
    )

    st.markdown("#### Bowling Style")
    st.metric(
        label="Right-arm medium",
        value="",
        border=True
    )

st.divider()


def find_opponent_team(row):
    return row["Team2"] if "V Kohli" in row['Team1Players'] else row["Team1"]

st.subheader(f"{selected_section}")

# Batting Section

if selected_section == "Batting Analysis":

    # innings played
    matches["Players"] = matches["Team1Players"] + matches["Team2Players"]
    innings_played = matches[matches["Players"].str.contains("V Kohli")].shape[0]

    # total runs scored
    total_runs_scored = balls[balls["batter"] == "V Kohli"]["batsman_run"].sum()

    # 50s and 100s
    vk_ball_by_ball = balls[balls["batter"] == "V Kohli"]
    vk_match_run = vk_ball_by_ball.groupby(["ID", "batter"])["batsman_run"].sum()

    num_half_century_scored = vk_match_run[(vk_match_run >= 50) & (vk_match_run < 100)].shape[0]
    num_century_scored = vk_match_run[(vk_match_run >= 100)].shape[0]

    num_half_century_scored = vk_match_run[(vk_match_run >= 50) & (vk_match_run < 100)].shape[0]
    num_century_scored = vk_match_run[(vk_match_run >= 100)].shape[0]

    # overall strike rate in IPL
    total_balls_played = vk_ball_by_ball.shape[0]
    strike_rate_ipl = round((total_runs_scored / total_balls_played) * 100, 2)

    # number of orange cap
    orange_cap_holders_season = balls.merge(matches[["ID", "Season"]], on="ID").groupby(["Season", "batter"])["batsman_run"].sum().reset_index().sort_values(by=["Season", "batsman_run"], ascending=[True, False]).drop_duplicates(subset="Season", keep="first")

    num_orange_cap = orange_cap_holders_season[orange_cap_holders_season["batter"] == "V Kohli"].shape[0]

    # high score
    vk_ball_by_ball_season = vk_ball_by_ball.merge(matches, on="ID")
    
    vk_ball_by_ball_season["OpponentTeam"] = vk_ball_by_ball_season.apply(find_opponent_team, axis=1)

    high_score = vk_ball_by_ball_season.groupby(["ID", "OpponentTeam"])["batsman_run"].sum().sort_values(ascending=False).head(1).reset_index().values[0][2]

    opponent_team = vk_ball_by_ball_season.groupby(["ID", "OpponentTeam"])["batsman_run"].sum().sort_values(ascending=False).head(1).reset_index().values[0][1]

    # 6s & 4s
    vk_six = vk_ball_by_ball_season[vk_ball_by_ball_season["batsman_run"] == 6]
    vk_sixes_season = vk_six.groupby("Season")["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Sixes"})

    vk_four = vk_ball_by_ball_season[vk_ball_by_ball_season["batsman_run"] == 4]
    vk_fours_season = vk_four.groupby("Season")["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Fours"})

    vk_boundaries = vk_fours_season.merge(vk_sixes_season, on="Season")

    num_fours, num_sixes= vk_boundaries.sum(numeric_only=True).values[0], vk_boundaries.sum(numeric_only=True).values[1]

    num_boundaries = num_fours + num_sixes

    batting_info = {
        0: ["Innings Played", innings_played],
        1:["Runs Scored", total_runs_scored],
        2:["Overall Strike Rate", strike_rate_ipl],
        3:["50s", num_half_century_scored],
        4:["100s", num_century_scored],
        5:["6s", num_sixes],
        6:["4s", num_fours],
        7:["Boundaries", num_boundaries],
        8:["Orange Cap", num_orange_cap],
        9:["High Score", high_score],
    }

    cols = st.columns(3)
    idx, i = 0, 0

    for idx in range(0, 3):
        with cols[idx]:
            for j in range(i, i+3):
                st.markdown(f"#### {batting_info[j][0]}")
                st.metric(
                    label=f"{batting_info[j][1]}",
                    value="",
                    border=True
                )
                if j == 2:
                    st.markdown(f"#### {batting_info[9][0]}")
                    st.metric(
                        label=f"{batting_info[9][1]} against PBKS (2016)",
                        value="",
                        border=True
                    )
            i += 3
    

    st.divider()

    # Runs Scored Per Season
    vk_seasonwise_run = vk_ball_by_ball_season.groupby("Season")["batsman_run"].sum().reset_index()
    fig = px.line(vk_seasonwise_run, x="Season", y="batsman_run", title="Season-wise Runs", markers=True, labels={"Season": "Season", "batsman_run": "Runs Scored"}, template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Season-wise Strike Rate
    vk_run_ball_season = vk_ball_by_ball_season.groupby(["Season"]).agg(
    {
        "ballnumber": "count",
        "batsman_run": "sum"
    }
    ).reset_index()

    vk_run_ball_season["strike_rate"] = round((vk_run_ball_season["batsman_run"] / vk_run_ball_season["ballnumber"]) * 100, 2)

    fig = px.line(vk_run_ball_season, x="Season", y="strike_rate", markers=True, labels={"Season": "Season", "strike_rate": "Strike Rate"}, title="Season-wise Strike Rate", template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Dismissal Type
    vk_dismissal_type=  vk_ball_by_ball_season.kind.value_counts().reset_index()
    fig = px.pie(vk_dismissal_type, names="kind", values="count", title="Dismissal Type", template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Top 5 Bowlers who dismissed Virat Kohli the most
    vk_ball_by_ball_season["isBowlerWicket"] = vk_ball_by_ball_season["kind"].apply(lambda x: 1 if x in ["caught", "bowled", "stumped", "caught and bowled", "lbw"] else 0)

    vk_wicket_bowler = vk_ball_by_ball_season.groupby("bowler").agg(
        {
            "batsman_run": "sum",
            "ballnumber": "count",
            "isBowlerWicket": "sum"
        }
    )

    vk_wicket_bowler["strike_rate"] = round((vk_wicket_bowler["batsman_run"] / vk_wicket_bowler["ballnumber"]) * 100, 2)

    most_dismissal_bowlers = vk_wicket_bowler.sort_values(by=["isBowlerWicket"], ascending=False).reset_index().head(5)

    fig = px.bar(
        most_dismissal_bowlers, 
        x="bowler", 
        y="isBowlerWicket",
        labels = {"bowler": "Bowler", "isBowlerWicket": "Total Wickets"},
        title = "Top 5 Bowlers",
        text_auto=True,
        custom_data = ["strike_rate"],
        template="plotly_dark"
    )


    for i, d in enumerate(fig.data[0]["customdata"]):
        fig.add_annotation(
            x = fig.data[0]['x'][i],
            y = fig.data[0]['y'][i] + 0.5,
            text = f"SR: {d[0]}",
            showarrow=False,
            font=dict(size=12, color="black")
        )

    st.plotly_chart(fig, use_container_width=True)

    # 6s and 4s Per Season
    fig = go.Figure(data = [
    go.Bar(name="Fours", x=vk_boundaries["Season"], y=vk_boundaries["Fours"], text=vk_boundaries["Fours"], textposition="inside"),
    go.Bar(name="Sixes", x=vk_boundaries["Season"], y=vk_boundaries["Sixes"], text=vk_boundaries["Sixes"], textposition="inside")
    ]
    )

    fig.update_layout(
        barmode="group",
        title="Number of 4s and 6s per Season",
        xaxis_title="Season",
        yaxis_title="Count",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Number of Boundaries
    vk_boundaries["Boundaries"] = vk_boundaries.sum(axis=1, numeric_only=True)
    fig = px.line(
        vk_boundaries,
        x="Season",
        y="Boundaries",
        title="Number of Boundaries per Season",
        markers=True,
        template = "plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Number of 50s and 100s Per Season
    vk_match_runs_season = vk_ball_by_ball_season.groupby(["Season", "ID"])["batsman_run"].sum().reset_index()
    vk_fifties_season = vk_match_runs_season[(vk_match_runs_season["batsman_run"] >= 50) & (vk_match_runs_season["batsman_run"] < 100)].groupby("Season")["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Fifties"})

    vk_hundreds_season = vk_match_runs_season[(vk_match_runs_season["batsman_run"] >= 100)].groupby("Season")["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Hundreds"})

    vk_fif_hun_season = vk_fifties_season.merge(vk_hundreds_season, how="left", on="Season")
    vk_fif_hun_season.fillna(0, inplace=True)

    fig = go.Figure(data=[
    go.Bar(name = "50s", x=vk_fif_hun_season["Season"], y=vk_fif_hun_season["Fifties"], text=vk_fif_hun_season["Fifties"], textposition="inside"),
    go.Bar(name = "100s", x=vk_fif_hun_season["Season"], y=vk_fif_hun_season["Fifties"], text=vk_fif_hun_season["Hundreds"], textposition="inside")
        ]
    )

    fig.update_layout(
        barmode="group",
        title = "Number of 50s and 100s per Season",
        xaxis_title = "Season",
        yaxis_title = "Count",
        template = "plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)
# Bowling Section
elif selected_section == "Bowling Analysis":
    # number of balls bowled
    num_balls_delivered = balls[balls["bowler"] == "V Kohli"].shape[0]

    # number of wickets
    vk_as_bowler = balls[balls["bowler"] == "V Kohli"].merge(matches, on="ID")
    vk_as_bowler["isBowlerWicket"] = vk_as_bowler.kind.apply(lambda x: 1 if x in ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'] else 0 )
    num_wickets = vk_as_bowler['isBowlerWicket'].sum()

    # overall economy in IPL
    vk_as_bowler["isLegalDelivery"] = vk_as_bowler.extra_type.apply(lambda x: 0 if x in ["wides", "noballs"] else 1)
    vk_as_bowler["BowlerRun"] = vk_as_bowler.extra_type.apply(lambda x: 0 if x in ["legbyes", "byes"] else 1) * vk_as_bowler.total_run

    runs_conceded = vk_as_bowler["BowlerRun"].sum()
    num_legal_deliveries = vk_as_bowler["isLegalDelivery"].sum()

    economy = round((runs_conceded / num_legal_deliveries) * 6, 2)

    bowling_info = {
        0: ["Balls Bowled", num_balls_delivered],
        1: ["Wickets Taken", num_wickets],
        2: ["Overall Economy", economy]
    }

    cols = st.columns(3)
    idx, i = 0, 0

    for idx in range(0, 3):
        with cols[idx]:
            for j in range(i, i+1):
                st.markdown(f"#### {bowling_info[j][0]}")
                st.metric(
                    label=f"{bowling_info[j][1]}",
                    value="",
                    border=True
                )
            i += 1
    

    st.divider()

    # Number of Balls Bowled Per Season
    fig = px.line(vk_as_bowler.groupby("Season")["ballnumber"].count().reset_index(),
        x="Season", y="ballnumber", markers=True, title="Number of Balls Bowled per Season",
        labels={"Season":"Season", "ballnumber": "Balls Bowled"},template = "plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Distribution of Balls
    fig = px.pie(vk_as_bowler.extra_type.replace(["legbyes", "byes", np.nan], "Normal").value_counts().reset_index(),
       names="extra_type", values="count",
       title="Distribution of Balls",
       template = "plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)
# Fielding Section
else:
    
    # number of catches and runouts
    vk_as_fielder = balls[balls.fielders_involved == "V Kohli"].merge(matches, on="ID")
    num_catches, num_of_runouts = vk_as_fielder["kind"].value_counts().values[0], vk_as_fielder["kind"].value_counts().values[1]

    fielding_info = {
        0: ["Catches Taken", num_catches],
        1: ["Runouts", num_of_runouts]
    }

    cols = st.columns(2)
    idx = 0

    for idx in range(0, 2):
        with cols[idx]:
            st.markdown(f"#### {fielding_info[idx][0]}")
            st.metric(
                label=f"{fielding_info[idx][1]}",
                value="",
                border=True
            )
    

    st.divider()

    # Catches Taken Per Season
    fig = px.bar(vk_as_fielder[vk_as_fielder.kind.isin(["caught"])].groupby("Season")["kind"].count().reset_index(),
       x="Season", y="kind", text_auto=True,
       title="Catches Taken Per Season",
       labels={"Season":"Season", "kind":"Catches Taken"}, template = "plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Runouts Per Season
    fig = px.bar(vk_as_fielder[vk_as_fielder.kind.isin(["run out"])].groupby("Season")["kind"].count().reset_index(),
       x="Season", y="kind", text_auto=True,
       title="Runouts Per Season",
       labels={"Season":"Season", "kind":"Runouts"}, template = "plotly_dark")

    st.plotly_chart(fig, use_container_width=True)
