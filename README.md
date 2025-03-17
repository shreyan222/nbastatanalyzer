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

Sample Results:

Final Standard Data Table (Sorted by Sorting Score):

Name                Position  Team  AgainstTeam  Stat           Line  Odds      H2HArray                  L5Array               Temp  Size  H2HAvg  L5Avg  Diff    Rel Diff  Percent  Sample Size  Score  GameId                             
Mikal Bridges       SG        NYK   MIA          Pts+Rebs+Asts  25.5  standard  [33, 35, 33, 41, 26, 17]  [12, 31, 26, 41, 28]  5     6     30.833  27.6   5.333   0.175     20.915   6            1.693  NBA_game_DSwyh9T6CVpOJ3McUhI0wF8d  
Mikal Bridges       SG        NYK   MIA          Pts+Asts       21.5  standard  [26, 28, 27, 32, 23, 13]  [9, 27, 23, 37, 22]   5     6     24.833  23.6   3.333   0.126     15.504   6            1.684  NBA_game_DSwyh9T6CVpOJ3McUhI0wF8d  
Mikal Bridges       SG        NYK   MIA          Points         17.5  standard  [21, 23, 24, 26, 17, 5]   [6, 22, 15, 33, 19]   4.5   6     19.333  19.0   1.833   0.081     10.476   6            1.617  NBA_game_DSwyh9T6CVpOJ3McUhI0wF8d  
Luka Doncic         PG        LAL   SAS          Rebounds       9.5   standard  [13, 12, 9, 10, 10, 6]    [7, 8, 12, 11, 11]    4.5   6     10.0    9.8    0.5     0.034     5.263    6            1.605  NBA_game_oeCCiNtypxK0snbnRGEdXxZ9  
Chris Paul          PG        SAS   LAL          Assists        6.5   standard  [4, 9, 11, 6, 10]         [7, 9, 9, 3, 6]       4.5   5     8.0     6.8    1.5     0.13      23.077   5            1.502  NBA_game_oeCCiNtypxK0snbnRGEdXxZ9  


For a more detailed view, check the example_results folder where output_data.csv is saved.



Notes

The data is sourced from APIs and websites like PrizePicks and StatMuse.

Testing.csv stores the scraped prop data.

data.json holds the copied API data.

Output is stored in output_data.csv for further use.

Currently in progress...

Plans to add additional advanced stats such as Defensive rankings & trades/injuries.


