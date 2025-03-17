NBA Prop Betting Analysis Project

This project is designed to scrape, process, and analyze NBA prop bet data. It fetches live props, compares them to historical performance, and assigns a score to determine the best betting opportunities.

Files Overview

1. PPnbapicks.py

Handles searching, filtering, and listing NBA prop bet data from Testing.csv.

Functions:

PropSearch(search_string): Searches for props containing a given string.

RemoveSearch(df, search_string): Removes rows containing a given string.

Lists(df, string): Extracts specific columns from the dataset based on the input parameter.

filter_rows_by_league_id(df, league_id): Filters props by league ID.

2. PPapiscraper.py

Scrapes and processes prop data from data.json, saves it to a database and CSV, and schedules updates.

Main Features:

Extracts display names and player stats from API data.

Saves filtered props.

I would use selenium/requests to automatically scrape data but I have been IP banned so you have to manually copy and paste into data.json by visiting https://api.prizepicks.com/projections.

3. dataFinder.py

Fetches player stats from StatMuse, including last 10 games and head-to-head stats.

Functions:

against_team(team): Determines the opponent of a given team.

stats_against_team_t_season(name, team, timeframe): Retrieves a player's stats against a team over a specific timeframe.

stats_ten_games(name): Fetches a player's last 10 game stats.

specific_stat_vs_opp_games_arr(arr, stat): Extracts a specific stat from historical data.

4. testalgo.py

Runs the main analysis, filters props, calculates scores, and organizes output data.

Main Workflow:

Loads and filters props based on various criteria.

Fetches team depth charts from ESPN.

Calculates H2H and L5 averages, differences, and sorting scores.

Outputs data in a formatted table and saves results to output_data.csv.

5. data.json

A JSON file where data from PrizePicks' public API (https://api.prizepicks.com/projections) is copied and stored for processing.

Installation & Usage

Prerequisites

pip install pandas requests beautifulsoup4 apscheduler unidecode pytz

Running the Scripts

Fetch and update prop data:

python PPapiscraper.py

Run the main analysis:

python testalgo.py

Notes

The data is sourced from APIs and websites like PrizePicks and StatMuse.

Testing.csv stores the scraped prop data.

data.json holds the copied API data.

Output is stored in output_data.csv for further use.

Currently in progress...

Plans to add additional advanced stats such as Defensive rankings & trades/injuries.
