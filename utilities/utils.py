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
def get_player_metrics(df, player_name, position):
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
