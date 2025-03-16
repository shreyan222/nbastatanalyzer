import sqlite3
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from prop import Prop
import pickle
import json
import time

def save_props_to_file(props, filename='props.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(props, f)
    print(f"Saved {len(props)} props to {filename}")


props_list = []


def extract_display_names(data):
    players = {}
    for item in data["included"]:
        if item["type"] == "new_player":
            player_id = item["id"]
            display_name = item["attributes"].get("display_name", "Unknown Player")
            position = item["attributes"].get("position", "No position")
            image_url = item["attributes"].get("image_url", "No Image URL")
            team = item["attributes"].get("team", "Unknown Team")
            league_id = item["relationships"]["league"]["data"]["id"] if "league" in item[
                "relationships"] else "Unknown League"
            players[player_id] = {'display_name': display_name,
                                  'position': position,
                                  'image_url': image_url,
                                  'league_id': league_id,
                                  'team': team}

    return players


def extract_player_stats(data, players):
    props = []
    game = False
    prizepicks_stats = []
    for item in data["data"]:
        if item["type"] == "projection":
            prop_id = item["id"]  # Capture the prop_id here
            player_id = item["relationships"]["new_player"]["data"]["id"]
            leg_id = item["relationships"]["league"]["data"]["id"]
            player_info = players.get(player_id, {
                'display_name': "Unknown Player",
                'position': "No position",
                'image_url': "No Image URL",
                'league_id': "Unknown League",
                'team': "Unknown Team"
            })
            line_score = item["attributes"]["line_score"]
            stat_type = item["attributes"]["stat_type"]
            start_time_str = item["attributes"]["start_time"]
            odds_type = item["attributes"]["odds_type"]

            if "game_id" in item["attributes"]:
                game_id = item["attributes"]["game_id"]
                game = True
            else:
                game_id = None

            # Convert start_time to UTC and format it
            if start_time_str:
                start_time_with_tz = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S%z')
                start_time_utc = start_time_with_tz.astimezone(pytz.utc)
                start_time_for_sqlite = start_time_utc.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_time_for_sqlite = None
            prop = Prop(player_name=player_info['display_name'],
                        position=player_info['position'],
                        stat_type=stat_type,
                        line_score=line_score,
                        odds_type=odds_type,
                        team_name=player_info['team'],
                        league_id=player_info['league_id'],
                        game_id=game_id)
            props.append(prop)
            if game:
                prizepicks_stats.append({
                    'Prop ID': prop_id,
                    'Player ID': player_id,
                    'Display Name': player_info['display_name'],
                    'Position': player_info['position'],
                    'Image Url': player_info['image_url'],
                    'Line Score': line_score,
                    'Stat Type': stat_type,
                    'League ID': player_info['league_id'],
                    'Team Name': player_info['team'],
                    'Adjusted Odds': False,
                    'Odds Type': odds_type,
                    'Game ID': game_id,
                    'Start Time': start_time_for_sqlite,
                })
            else:
                prizepicks_stats.append({
                    'Prop ID': prop_id,
                    'Player ID': player_id,
                    'Display Name': player_info['display_name'],
                    'Position': player_info['position'],
                    'Image Url': player_info['image_url'],
                    'Line Score': line_score,
                    'Stat Type': stat_type,
                    'League ID': player_info['league_id'],
                    'Team Name': player_info['team'],
                    'Adjusted Odds': False,
                    'Odds Type': odds_type,
                    'Start Time': start_time_for_sqlite,
                })

    return prizepicks_stats, props


def fetch_and_update_data():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    global props_list
    prizepicks_stats = []
    conn = sqlite3.connect('prizepicks_stats.db')
    cursor = conn.cursor()

    try:

        '''driver.get("https://api.prizepicks.com/projections")
        time.sleep(30)
        json_data = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(json_data)'''

        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        print(data)  # Verify the structure'''

        players = extract_display_names(data)
        prizepicks_stats, props = extract_player_stats(data, players)
        prizepicks_stats_df = pd.DataFrame(prizepicks_stats)
        prizepicks_stats_df = prizepicks_stats_df.sort_values(by=["Display Name", "Stat Type"])

        props_list = props
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(prizepicks_stats_df)
        prizepicks_stats_df.to_csv('Testing.csv')
        print(f"Number of props: {len(props)}")

        for prop in props:
            # Assuming calculate_score is a method in Prop
            print(prop)
        save_props_to_file(props)
        nba_props = [
            prop for prop in props
            if prop.league_id == "7" and not (
                    prop.stat_type.lower() in {"dunks", "fantasy score"} or "combo" in prop.stat_type.lower()
            )
        ]

        # Save filtered props to pickle file
        save_props_to_file(nba_props, 'nba_props.pkl')

        print(f"Saved {len(nba_props)} NBA props to nba_props.pkl")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        #driver.quit()
        conn.close()


def get_props():
    fetch_and_update_data()  # Fetch data when needed
    return props_list


if __name__ == "__main__":
    fetch_and_update_data()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_update_data, 'interval', minutes=7)
    scheduler.start()
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
