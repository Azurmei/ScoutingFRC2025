
import pandas as pd
from collections import Counter

pd.options.mode.chained_assignment = None
pd.set_option('future.no_silent_downcasting', True)

auto_score = {
    'auto_fuel_count': 1,
    'auto_hang': 15,
}

tele_score = {
    'tele_fuel_count': 1,
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
    hash = Counter(tmp)
    return hash.most_common(1)[0][0]


# --------
# Get Average points scored in match - AUTO
# --------
def average_auto_points(df:pd.DataFrame) -> float:
    selected_cols = ['auto_fuel_count', 'auto_hang']
    selected_df = df[selected_cols].copy()

    selected_df[selected_cols] = selected_df[selected_cols].apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df['auto_hang'] *= auto_score['auto_hang']

    return selected_df.sum(axis=1).mean()

# --------
# Get Average points scored in match - TELEOP
# --------
def average_teleop_points(df:pd.DataFrame) -> float:
    selected_cols = ['tele_fuel_count']
    selected_df = df[selected_cols].copy()

    selected_df[selected_cols] = selected_df[selected_cols].apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['tele_fuel_count'] *= tele_score['tele_fuel_count']

    return selected_df.sum(axis=1).mean()

# --------
# match vs points graph data
# --------
def match_point_graph_data(df:pd.DataFrame) -> pd.Series:
    selected_cols = ['auto_fuel_count', 'tele_fuel_count', 'end_hang']
    selected_df = df[selected_cols].copy()

    selected_df[selected_cols] = selected_df[selected_cols].apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    selected_df['auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df['tele_fuel_count'] *= tele_score['tele_fuel_count']
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
    alliance = ['alliance1', 'alliance2']

    scores_df = match_point_graph_data(df)
    alliance_df = df.loc[:,alliance]

    max_score_index = scores_df.idxmax()
    alliance_partners = alliance_df.loc[max_score_index]

    return alliance_partners.to_string(index=False, header=False).replace("\n", " , ")

# --------
# Highest Score
# --------
def highest_score(df:pd.DataFrame) -> float:
    scores_df = match_point_graph_data(df)
    return scores_df.max()

# --------
# Highest number of wins with alliance
# --------
def best_alliance(df:pd.DataFrame):
    selected_cols = ['alliance1', 'alliance2', 'result']
    selected_df = df[selected_cols]

    selected_df = selected_df[selected_df['result'] == "Win"]

    team_wins = pd.concat(
        [selected_df['alliance1'], selected_df['alliance2']]
    ).value_counts()

    return team_wins.sort_values(ascending=False)

def select_graph_by_match(team_data:pd.DataFrame, select_metric:str):
    return pd.to_numeric(team_data[select_metric], errors='coerce')

# --------
# Average fuel scored in matches
# --------
def average_fuel_scored(df:pd.DataFrame) -> float:
    selected_cols = ["auto_fuel_count", "tele_fuel_count"]
    selected_df = df[selected_cols].copy()

    selected_df[selected_cols] = selected_df[selected_cols].apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0)
    )

    total_sum = selected_df.sum().sum()
    num_matches = len(selected_df)

    return total_sum / num_matches if num_matches > 0 else 0

