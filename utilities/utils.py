import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import glob
import os
custom_fontt = fm.FontProperties(fname="fonts/Alexandria-Regular.ttf")


def load_data(folder_path):

    all_data = []
    for file in glob.glob(folder_path):
        df = pd.read_csv(file)
        # Extracting the file name without extension as 'league' column
        df['League'] = os.path.splitext(os.path.basename(file))[0]
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    return combined_df

# Helper function to get players by position
def get_players_by_position(df, league, position):
    if league!='All':
        df = df[df['League'] == league]    
    return df[df['Primary Position'] == position]['Name'].tolist()

def get_player_metrics_percentile_ranks(df, player_name, position):
    position_specific_data = df[df['Primary Position'] == position]
    numeric_columns = position_specific_data.select_dtypes(include=np.number)
    non_numeric_columns = position_specific_data.select_dtypes(exclude=np.number)

    # Perform percentile ranking (only for numeric columns)
    positional_percentile_data = numeric_columns.rank(pct=True, axis=0) * 100

    # Combine the ranked numeric data with the non-numeric columns
    result = pd.concat([non_numeric_columns.reset_index(drop=True), positional_percentile_data.reset_index(drop=True)], axis=1)
    player_data = result[result['Name'] == player_name]

    if not player_data.empty:
        return player_data
    return None

def get_avg_metrics_percentile_ranks(df, position):
    position_specific_data = df[df['Primary Position'] == position]
    numeric_columns = position_specific_data.select_dtypes(include=np.number)
    non_numeric_columns = position_specific_data.select_dtypes(exclude=np.number)

    # Step 2: Calculate mean of each column
    column_means = numeric_columns.mean()

    # Step 3: Create a new row for the average values
    avg_row = {col: column_means[col] for col in numeric_columns.columns}
    avg_row['Name'] = 'AVG'
    avg_row['Primary Position'] = None  # Non-numeric fields set to None

    # Create a DataFrame for the average row
    avg_df = pd.DataFrame([avg_row], columns=df.columns)

    # Step 4: Combine the original DataFrame with the average row
    df_with_avg = pd.concat([df, avg_df], ignore_index=True)

    # Calculate percentile ranks including the average row
    positional_percentile_data = df_with_avg[numeric_columns.columns].rank(pct=True, axis=0) * 100

    # Prepare the average metrics DataFrame
    avg_data = avg_df.copy()
    avg_data[numeric_columns.columns] = positional_percentile_data.loc[df_with_avg['Name'] == 'AVG'].values.flatten()
    
    return avg_data

def get_player_and_avg_metrics(df, player_name, position):
    # Get player metrics
    player_metrics = get_player_metrics_percentile_ranks(df, player_name, position)
    
    # Get average metrics
    avg_metrics = get_avg_metrics_percentile_ranks(df, position)
    
    print(player_metrics)
    print(avg_metrics)

    return player_metrics, avg_metrics

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