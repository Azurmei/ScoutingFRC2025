import pandas as pd
from collections import Counter

pd.options.mode.chained_assignment = None
pd.set_option('future.no_silent_downcasting', True)

auto_score = {
    'auto_fuel_count': 1,
    'auto_hang': 15,
}

tele_score = {
    'teleop_fuel_count': 1,
}

end_score = {
    'end_hang': 10,
}

headers = ['auto_leave','auto_hang','teleop_fuel_count','end_hang']

# --------
# Get Priority of game piece for team
# --------
def get_priority(df:pd.DataFrame) -> str:
    tmp = df["game_priority"]
    return Counter(tmp).most_common(1)[0][0]

# --------
# Get average rp for each match from a team
# --------
def average_rp(df:pd.DataFrame) -> float:
    selected_df = df[['energized_rp', 'supercharged_rp', 'traversal_rp', 'result']].copy()

    selected_df[['energized_rp','supercharged_rp','traversal_rp']] = \
        selected_df[['energized_rp','supercharged_rp','traversal_rp']].replace({'TRUE':1,'FALSE':0})

    selected_df['result'] = selected_df['result'].map({
        "Win":3,
        "tied":1,
        "Loss":0
    })

    return selected_df.sum(axis=1).mean()

# --------
# Get Average points scored in match - AUTO
# --------
def average_auto_points(df:pd.DataFrame) -> float:
    selected_df = df[['auto_fuel_count','auto_hang']].copy()

    selected_df = selected_df.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df['auto_hang'] *= auto_score['auto_hang']

    return selected_df.sum(axis=1).mean()

# --------
# Get Average points scored in match - TELEOP
# --------
def average_teleop_points(df:pd.DataFrame) -> float:
    selected_df = df[['teleop_fuel_count']].copy()

    selected_df = selected_df.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['teleop_fuel_count'] *= tele_score['teleop_fuel_count']

    return selected_df.sum(axis=1).mean()

# --------
# match vs points graph data
# --------
def match_point_graph_data(df:pd.DataFrame) -> pd.Series:
    selected_df = df[['auto_fuel_count','teleop_fuel_count','end_hang']].copy()

    selected_df = selected_df.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df['teleop_fuel_count'] *= tele_score['teleop_fuel_count']
    selected_df['end_hang'] *= end_score['end_hang']

    return selected_df.sum(axis=1)

# --------
# match vs W/L graph data
# --------
def match_win_loss_graph_data(df: pd.DataFrame) -> pd.Series:
    return df['result'].map({
        "Win": 1,
        "Loss": -1,
        "tied": 0
    })

# --------
# W/L ratio data
# --------
def win_percentage(df: pd.DataFrame) -> float:
    total = len(df)
    if total == 0:
        return 0.0

    wins = df['result'].apply(lambda x: 1 if x == "Win" else 0).sum()
    return (wins / total) * 100

# --------
# Highest score alliance teams
# --------
def highest_score_alliance(df:pd.DataFrame) -> str:
    scores_df = match_point_graph_data(df)
    alliance_df = df[['alliance1','alliance2']]

    max_index = scores_df.idxmax()
    partners = alliance_df.loc[max_index]

    return partners.to_string(index=False, header=False).replace("\n"," , ")

# --------
# Highest Score
# --------
def highest_score(df:pd.DataFrame) -> float:
    scores_df = match_point_graph_data(df)
    return scores_df.max()

# --------
# Highest number of wins with alliance
# --------
def best_alliance(df:pd.DataFrame) -> pd.Series:
    selected_df = df[['alliance1','alliance2','result']]
    selected_df = selected_df[selected_df['result'] == "Win"]

    team_wins = pd.concat([selected_df['alliance1'],selected_df['alliance2']]).value_counts()
    return team_wins.sort_values(ascending=False)

def select_graph_by_match(team_data:pd.DataFrame, select_metric:str) -> pd.Series:
    return pd.to_numeric(team_data[select_metric], errors="coerce").fillna(0)

# --------
# Average fuel scored in matches
# --------
def average_fuel_scored(df:pd.DataFrame) -> float:
    selected_df = df[['auto_fuel_count','teleop_fuel_count']].copy()

    selected_df = selected_df.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    total = selected_df.sum().sum()
    matches = len(selected_df)

    return total / matches if matches > 0 else 0