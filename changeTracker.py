import sqlite3
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import pytz
import json
from copy import deepcopy


class PropChangeTracker:
    def __init__(self, db_path='prizepicks_stats.db', interval_minutes=5):
        self.db_path = db_path
        self.interval_minutes = interval_minutes
        self.previous_props = None
        self.scheduler = BackgroundScheduler()
        self.setup_display_options()

    def setup_display_options(self):
        # Set pandas display options for better visibility
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

    def load_data(self):
        """Load data from the data.json file"""
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def extract_display_names(self, data):
        """Extract player information from the data"""
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

    def extract_player_stats(self, data, players):
        """Extract player stats and props from the data"""
        props = []
        for item in data["data"]:
            if item["type"] == "projection":
                prop_id = item["id"]
                player_id = item["relationships"]["new_player"]["data"]["id"]
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

                # Handle game_id if present
                game_id = item["attributes"].get("game_id", None)

                # Convert start time to UTC
                if start_time_str:
                    start_time_with_tz = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S%z')
                    start_time_utc = start_time_with_tz.astimezone(pytz.utc)
                    start_time_for_sqlite = start_time_utc.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    start_time_for_sqlite = None

                # Create prop dictionary with all relevant information
                prop = {
                    'Prop ID': prop_id,
                    'Player ID': player_id,
                    'Display Name': player_info['display_name'],
                    'Position': player_info['position'],
                    'Line Score': line_score,
                    'Stat Type': stat_type,
                    'League ID': player_info['league_id'],
                    'Team Name': player_info['team'],
                    'Odds Type': odds_type,
                    'Game ID': game_id,
                    'Start Time': start_time_for_sqlite,
                }

                props.append(prop)

        return props

    def filter_nba_props(self, props):
        """Filter only NBA props (League ID = 7) and exclude certain stat types"""
        return [
            prop for prop in props
            if prop['League ID'] == "7" and not (
                    prop['Stat Type'].lower() in {"dunks", "fantasy score"} or "combo" in prop['Stat Type'].lower()
            )
        ]

    def compare_props(self, previous_props, current_props):
        """Compare previous and current props to detect changes"""
        if previous_props is None:
            return {
                "new_props": current_props,
                "removed_props": [],
                "changed_props": []
            }

        # Create dictionaries for easy lookup by Prop ID
        prev_props_dict = {prop.get('Prop ID', ''): prop for prop in previous_props if 'Prop ID' in prop}
        curr_props_dict = {prop.get('Prop ID', ''): prop for prop in current_props if 'Prop ID' in prop}

        # Remove empty keys if any
        if '' in prev_props_dict:
            prev_props_dict.pop('')
        if '' in curr_props_dict:
            curr_props_dict.pop('')

        # Find new props (in current but not in previous)
        new_prop_ids = set(curr_props_dict.keys()) - set(prev_props_dict.keys())
        new_props = [curr_props_dict[prop_id] for prop_id in new_prop_ids]

        # Find removed props (in previous but not in current)
        removed_prop_ids = set(prev_props_dict.keys()) - set(curr_props_dict.keys())
        removed_props = [prev_props_dict[prop_id] for prop_id in removed_prop_ids]

        # Find changed props (in both but with different values)
        changed_props = []
        for prop_id in set(prev_props_dict.keys()) & set(curr_props_dict.keys()):
            prev_prop = prev_props_dict[prop_id]
            curr_prop = curr_props_dict[prop_id]

            changes = {}
            # Check each key that we want to track changes for
            for key in ['Line Score', 'Stat Type', 'Odds Type']:
                # Only compare if both props have the key
                if key in prev_prop and key in curr_prop:
                    if prev_prop[key] != curr_prop[key]:
                        changes[key] = {
                            'previous': prev_prop[key],
                            'current': curr_prop[key]
                        }

            if changes:
                changed_props.append({
                    'Prop ID': prop_id,
                    'Player': curr_prop.get('Display Name', 'Unknown Player'),
                    'Team': curr_prop.get('Team Name', 'Unknown Team'),
                    'Stat Type': curr_prop.get('Stat Type', 'Unknown Stat'),
                    'Odds Type': curr_prop.get('Odds Type', 'Unknown Odds'),
                    'Changes': changes
                })

        return {
            "new_props": new_props,
            "removed_props": removed_props,
            "changed_props": changed_props
        }

    def print_changes(self, changes):
        """Print the detected changes in a readable format"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n====== PROP CHANGES DETECTED AT {timestamp} ======")

        # Print removed props
        if changes["removed_props"]:
            print("\n--- REMOVED PROPS ---")
            for prop in changes["removed_props"]:
                print(
                    f"• {prop['Display Name']} ({prop['Team Name']}) - ({prop['Odds Type']}) {prop['Stat Type']} {prop['Line Score']}")

        # Print new props
        if changes["new_props"]:
            print("\n--- NEW PROPS ---")
            for prop in changes["new_props"]:
                print(
                    f"• {prop['Display Name']} ({prop['Team Name']}) - ({prop['Odds Type']}) {prop['Stat Type']} {prop['Line Score']}")

        # Print changed props
        if changes["changed_props"]:
            print("\n--- CHANGED PROPS ---")
            for prop in changes["changed_props"]:
                # Using get() method to safely access values that might be missing
                player = prop.get('Player', 'Unknown Player')
                team = prop.get('Team', 'Unknown Team')
                print(f"• {player} ({team}):")
                for change_type, values in prop.get('Changes', {}).items():
                    previous = values.get('previous', 'N/A')
                    current = values.get('current', 'N/A')
                    print(f"  - {change_type}: {previous} → {current}")

        # If no changes were detected
        if not (changes["removed_props"] or changes["new_props"] or changes["changed_props"]):
            print("No changes detected.")

        print(f"======================================================\n")

    def log_changes_to_csv(self, changes):
        """Log all changes to a CSV file for record keeping"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Log removed props
        if changes["removed_props"]:
            df_removed = pd.DataFrame(changes["removed_props"])
            df_removed['Change Type'] = 'Removed'
            df_removed['Timestamp'] = timestamp
            df_removed.to_csv(f'prop_changes_{timestamp}_removed.csv', index=False)

        # Log new props
        if changes["new_props"]:
            df_new = pd.DataFrame(changes["new_props"])
            df_new['Change Type'] = 'New'
            df_new['Timestamp'] = timestamp
            df_new.to_csv(f'prop_changes_{timestamp}_new.csv', index=False)

        # Log changed props (requires flattening the changes dictionary)
        if changes["changed_props"]:
            # Create a more detailed log for changed props
            changed_records = []
            for prop in changes["changed_props"]:
                for change_type, values in prop['Changes'].items():
                    changed_records.append({
                        'Prop ID': prop['Prop ID'],
                        'Player': prop['Player'],
                        'Team': prop['Team'],
                        'Change Type': change_type,
                        'Previous Value': values['previous'],
                        'Current Value': values['current'],
                        'Timestamp': timestamp
                    })

            if changed_records:
                df_changed = pd.DataFrame(changed_records)
                df_changed.to_csv(f'prop_changes_{timestamp}_modified.csv', index=False)

    def check_for_changes(self):
        """Main function to check for changes in props"""
        try:
            data = self.load_data()
            if not data:
                return

            players = self.extract_display_names(data)
            all_props = self.extract_player_stats(data, players)
            nba_props = self.filter_nba_props(all_props)

            # Compare with previous props
            changes = self.compare_props(self.previous_props, nba_props)
            self.print_changes(changes)
            self.log_changes_to_csv(changes)

            # Update previous props for next comparison
            self.previous_props = deepcopy(nba_props)

        except Exception as e:
            print(f"Error checking for changes: {e}")

    def start(self):
        """Start the prop tracker"""
        print(f"Starting NBA Props Tracker. Checking for changes every {self.interval_minutes} minutes...")

        # Run once immediately to get initial data
        self.check_for_changes()

        # Schedule regular checks
        self.scheduler.add_job(self.check_for_changes, 'interval', minutes=self.interval_minutes)
        self.scheduler.start()

        try:
            # Keep the script running
            while True:
                time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            print("Stopping NBA Props Tracker...")
            self.scheduler.shutdown()
            print("Tracker stopped.")


if __name__ == "__main__":
    tracker = PropChangeTracker(interval_minutes=5)  # Check every 5 minutes
    tracker.start()
