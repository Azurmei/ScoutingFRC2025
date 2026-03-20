import pandas as pd
from collections import Counter

pd.options.mode.chained_assignment = None
pd.set_option('future.no_silent_downcasting', True)

auto_score = {
    'auto_fuel_count':      1,
    'auto_hang':      15,
}

tele_score = {
    'teleop_fuel_count':      1,
}

end_score = {
    'end_hang':     10,
}

headers = ['auto_leave','auto_hang',	'tele_fuel_count',	'end_hang',	]

# --------
# Get average rp for each match from a team
# --------
def average_rp(df:pd.DataFrame) -> float:
    selected_cols = ['energized_rp', 'supercharged_rp', 'traversal_rp', 'win', 'loss']
    selected_df = df[selected_cols]
    selected_df.loc[:,selected_cols] = selected_df.replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'win'] *= 3
    row_sums = selected_df.sum(axis=1)
    average_row_sum = row_sums.mean()
    return average_row_sum

# --------
# Get Average points scored in match - AUTO
# --------
def average_auto_points(df:pd.DataFrame) -> float:
    selected_cols = ['auto_fuel_count', 'auto_hang']

    col_int = ['auto_fuel_count', 'auto_hang']

    selected_df = df[selected_cols]

    selected_df.loc[:,col_int] = selected_df[col_int].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))
    

    # multiply scored with points 
    selected_df.loc[:,'auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df.loc[:,'auto_hang'] *= auto_score['auto_hang']                                                                
    

    # compute sums of each match auto
    row_sum = selected_df.sum(axis=1)
    average_row_sum = row_sum.mean()

    return average_row_sum

# --------
# Get Average points scored in match - TELEOP
# --------
def average_teleop_points(df:pd.DataFrame) -> float:
    selected_cols = ['tele_fuel_count']

    selected_df = df[selected_cols]

    selected_df.loc[:,selected_cols] = selected_df[selected_cols].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))

    # multiply scored with points
    selected_df.loc[:,'tele_fuel_count'] *= tele_score['tele_fuel_count']
    

    # compute sums of each match teleop
    row_sum = selected_df.sum(axis=1)
    average_row_sum = row_sum.mean()

    return average_row_sum


    def end_score(df:pd.DataFrame) -> float:
        selected_cols = ['end_hang']

        selected_df = df[selected_cols]

        selected_df.loc[:,selected_cols] = selected_df[selected_cols].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))

        # multiply scored with points
        selected_df.loc[:,'end_hang'] *= end_score['end_hang']
        

        # compute sums of each match teleop
        row_sum = selected_df.sum(axis=1)
        average_row_sum = row_sum.mean()

        return average_row_sum
    
    

# --------
# match vs points graph data
# --------
def match_point_graph_data(df:pd.DataFrame) -> pd.DataFrame:
    selected_col = ['auto_fuel_count', 'tele_fuel_count',  'end_hang']
    
    col_int = ['auto_fuel_count','tele_fuel_count']
    
    selected_df = df[selected_col]

  

    # convert cols from str to int
    selected_df.loc[:,col_int] = selected_df[col_int].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))

    # score points from cols
    selected_df.loc[:,'auto_fuel_count'] *= auto_score['auto_fuel_count']
    selected_df.loc[:,'tele_fuel_count'] *= tele_score['tele_fuel_count']

    # return dataframe
    return selected_df.sum(axis=1)

# --------
# match vs W/L graph data
# --------
def match_win_loss_graph_data(df:pd.DataFrame) -> pd.DataFrame:
    selected_col = ['win', 'loss']
    selected_df = df[selected_col]

    selected_df.loc[:,'win'] = selected_df['win'].replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'loss'] = selected_df['loss'].replace({'TRUE': -1, 'FALSE': 0})
    
    selected_df.loc[:,'result'] = selected_df['win'] + selected_df['loss']

    return selected_df['result']


# --------
# W/L ratio data
# --------
def win_percentage(df:pd.DataFrame) -> float:
    selected_col = ['win']
    selected_df = df[selected_col]

    selected_df.loc[:,'win'] = selected_df['win'].replace({'TRUE': 1, 'FALSE': 0})

    wins = selected_df['win'].sum()
    total = len(selected_df['win'])
    
    return (wins/total) * 100


# --------
# Highest score allaince teams
# --------
def highest_score_alliance(df:pd.DataFrame) -> str:
    
    alliance = ['alliance1', 'alliance2']

    scores_df = match_point_graph_data(df)
    alliance_df = df.loc[:,alliance]

    max_score_index = scores_df.idxmax()

    allaince_partners = alliance_df.loc[max_score_index]
    return allaince_partners.to_string(index=False, header=False).replace("\n", " , ") # for some reason to_string puts df into the string "Team\nTeam"
    

# --------
# Highest Score
# --------
def highest_score(df:pd.DataFrame) -> str:
    scores_df = match_point_graph_data(df)
    max_score_index = scores_df.idxmax()
    return scores_df.loc[max_score_index]

# --------
# Highest number of wins with allaince
# --------
def best_alliance(df:pd.DataFrame) -> str:
    selected_cols = ['alliance1', 'alliance2', 'win']
    selected_df = df[selected_cols]
    selected_df = selected_df[selected_df['win'] == 'TRUE']
    team_wins = pd.concat([selected_df['alliance1'], selected_df['alliance2']]).value_counts()
    sorted_team_wins = team_wins.sort_values(ascending=False)
    return sorted_team_wins

def select_graph_by_match(team_data:pd.DataFrame, select_metric:str) -> pd.DataFrame:
    return team_data[select_metric]

# --------
# Average fuel scored in matches
# --------
def average_fuel_scored(df:pd.DataFrame) -> float:
    selected_cols = ["auto_fuel_count", "tele_fuel_count",]
    selected_df = df[selected_cols]
    selected_df.loc[:,selected_cols] = selected_df[selected_cols].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))
    selected_df = selected_df.reset_index(drop=True)
    total_sum = selected_df.sum().sum()
    num_matches = selected_df.shape[0]
    average = total_sum / num_matches
    return average




    