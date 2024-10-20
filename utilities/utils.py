import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
custom_fontt = fm.FontProperties(fname="fonts/Alexandria-Regular.ttf")


def load_data(file_path):
    return pd.read_csv(file_path)

# Helper function to get players by position
def get_players_by_position(df, position):
    return df[df['Primary Position'] == position]['Name'].tolist()

# Helper function to get player metrics
def get_player_metrics_percentile_ranks(df, player_name, position):
    position_specific_data = df[df['Primary Position'] == position]
    numeric_columns = position_specific_data.select_dtypes(include=np.number)
    non_numeric_columns = position_specific_data.select_dtypes(exclude=np.number)

    # Perform percentile ranking (only for numeric columns)
    positional_percentile_data = numeric_columns.rank(pct=True, axis=1) * 100

    # Combine the ranked numeric data with the non-numeric columns
    result = pd.concat([non_numeric_columns, positional_percentile_data], axis=1)
    player_data = result[result['Name'] == player_name]

    if not player_data.empty:
        return player_data
    return None

import pandas as pd

def get_player_metrics_positional_mean(df, player_name, position):
    # Filter data for the specified position
    position_specific_data = df[df['Primary Position'] == position]
    
    if position_specific_data.empty:
        raise ValueError(f"No data found for position: {position}")
        
    positional_means = position_specific_data.mean(numeric_only=True).round(2)

    player_metrics = position_specific_data[position_specific_data['Name'] == player_name]

    if player_metrics.empty:
        raise ValueError(f"No data found for player: {player_name}")

    player_metrics = player_metrics.select_dtypes(include='number')
    
    # Instead of append, use pd.concat
    player_metrics_df = pd.DataFrame(columns=positional_means.index)
    player_metrics_df = pd.concat([player_metrics_df, player_metrics], ignore_index=True)

    positional_means_df = pd.DataFrame([positional_means], columns=positional_means.index)

    return player_metrics_df, positional_means_df

def get_stat_values(all_metrics, player_metrics_df, positional_means_df):
    stat1 = []
    stat2 = []

    for metric in all_metrics:
        # Append value from player_metrics_df or None if metric doesn't exist
        if metric in player_metrics_df.columns:
            stat1.append(player_metrics_df[metric].values[0])  # Get value from player_metrics_df
        else:
            stat1.append(None)  # Or handle as needed

        # Append value from positional_means_df or None if metric doesn't exist
        if metric in positional_means_df.columns:
            stat2.append(positional_means_df[metric].values[0])  # Get value from positional_means_df
        else:
            stat2.append(None)  # Or handle as needed
            
    return stat1, stat2