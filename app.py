import streamlit as st
import requests
import pandas as pd

# Function to fetch La Liga standings from the API
def get_laliga_standings():
    url = "https://laliga-standings.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "0792a56be6msh8f7c13ed3a6b2f2p1d72fajsn0a85f537fea0",
        "X-RapidAPI-Host": "laliga-standings.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to fetch Premier League standings from the API
def get_premier_league_standings():
    url = "https://premier-league-standings1.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "0792a56be6msh8f7c13ed3a6b2f2p1d72fajsn0a85f537fea0",
        "X-RapidAPI-Host": "premier-league-standings1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Main function to create the Streamlit app
def main():
    st.markdown(
        "<style>"
        "body { background-color: #f5f5f5; font-family: 'Poppins', sans-serif; }"
        "h1 { color: #ffffff; text-align: center; }"
        "table { font-family: 'Poppins', sans-serif; border-collapse: collapse; width: 100%; border-radius: 10px; overflow: hidden; }"
        ".la-liga th { background-color: #003472; color: white; font-weight: bold; padding: 15px 10px 15px 10px; font-family: 'Poppins', sans-serif;}"
        ".premier-league th { background-color: #3d195b; color: white; font-weight: bold; padding: 15px 10px 15px 10px; font-family: 'Poppins', sans-serif;}"
        "th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }"
        "</style>",
        unsafe_allow_html=True
    )

    # Navigation bar to select the league
    league = st.sidebar.selectbox("Select League", ["La Liga", "Premier League"])

    if league == "La Liga":
        display_laliga_standings()
    elif league == "Premier League":
        display_premier_league_standings()

# Function to display La Liga standings in a table using Streamlit
def display_laliga_standings():
    st.header("La Liga Standings")
    standings = get_laliga_standings()
    display_standings(standings, "la-liga")  # Pass the league class for styling

# Function to display Premier League standings in a table using Streamlit
def display_premier_league_standings():
    st.header("Premier League Standings")
    standings = get_premier_league_standings()
    display_standings(standings, "premier-league")  # Pass the league class for styling

# Function to display standings in a table using Streamlit
def display_standings(standings, league_class):
    data = []
    for team_data in standings:
        team = team_data['team']
        stats = team_data['stats']
        # Load team logo image
        team_logo = f'<img style="margin-right: 10px;" src="{team["logo"]}" width="30" height="30">'
        row = {
            'Rank': stats["rank"],
            'Team': f"<div style='display: flex; align-items: center; width: 100%;'>{team_logo} <span>{team['name']}</span></div>",
            'GP': stats["gamesPlayed"],
            'Wins': stats["wins"],
            'Draws': stats["ties"],
            'Losses': stats["losses"],
            'GF': stats["goalsFor"],
            'GA': stats["goalsAgainst"],
            'GD': stats["goalDifference"],
            'Points': stats["points"],
            'Abbreviation': team["abbreviation"]
        }
        data.append(row)

    df = pd.DataFrame(data)
    df_html = df.to_html(escape=False, index=False)
    # Apply CSS style to make the table smaller and change header color based on league
    df_html = df_html.replace('<table', f'<table class="{league_class}" style="font-size: 12px;"')
    df_html = df_html.replace('<th>Team</th>', '<th style="text-align: center;">Team</th>')
    st.markdown(df_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()