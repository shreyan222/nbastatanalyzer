import pandas as pd
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('Testing.csv')

def PropSearch(search_string):
    for column in df.columns:
        filtered_df = df[df[column].astype(str).str.contains(search_string, na=False)]

        if not filtered_df.empty:
            return(filtered_df)
def RemoveSearch(df, search_string):
    escaped_search_string = re.escape(search_string)

    masks = []

    for column in df.columns:
        mask = ~df[column].astype(str).str.contains(escaped_search_string, case=False, na=False)

        masks.append(mask)

    combined_mask = pd.DataFrame(masks).all(axis=0)

    filtered_df = df[combined_mask]

    return filtered_df
def Lists(df,string):
    prop_id_list = []
    player_id_list = []
    display_name_list = []
    image_url_list = []
    line_score_list = []
    stat_type_list = []
    league_id_list = []
    league_list = []
    adjusted_odds_list = []
    odds_type_list = []
    start_time_list = []
    team_list = []
    gameid_list = []
    position_list = []

    for column in df.columns:
        if column == 'Prop ID':
            prop_id_list = df[column].tolist()
        elif column == 'Player ID':
            player_id_list = df[column].tolist()
        elif column == 'Display Name':
            display_name_list = df[column].tolist()
        elif column == 'Image Url':
            image_url_list = df[column].tolist()
        elif column == 'Line Score':
            line_score_list = df[column].tolist()
        elif column == 'Stat Type':
            stat_type_list = df[column].tolist()
        elif column == 'League ID':
            league_id_list = df[column].tolist()
        elif column == 'League':
            league_list = df[column].tolist()
        elif column == 'Adjusted Odds':
            adjusted_odds_list = df[column].tolist()
        elif column == 'Odds Type':
            odds_type_list = df[column].tolist()
        elif column == 'Start Time':
            start_time_list = df[column].tolist()
        elif column == 'Team Name':
            team_list = df[column].tolist()
        elif column == 'Game ID':
            gameid_list = df[column].tolist()
        elif column == 'Position':
            position_list = df[column].tolist()

    if (string == "lineScore"):
        return line_score_list
    elif (string == "StatType"):
        return stat_type_list
    elif (string == "Name"):
        return display_name_list
    elif (string == "OddType"):
        return odds_type_list
    elif (string == "LeagueID"):
        return league_id_list
    elif (string == "TeamName"):
        return team_list
    elif (string == "GameID"):
        return gameid_list
    elif (string == "Position"):
        return position_list
    elif (string == "ImageURL"):
        return image_url_list



name_list = Lists(df,"Name")
line = Lists(df,"LineScore")
stat = Lists(df, "StatType")
odds = Lists(df,"OddType")
def filter_rows_by_league_id(df, league_id):
    filtered_rows = []

    for index, row in df.iterrows():
        if row['League ID'] == league_id:
            filtered_rows.append(row)

    filtered_df = pd.concat(filtered_rows, axis=1).transpose()

    return filtered_df