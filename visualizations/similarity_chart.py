
import plotly.graph_objects as go
from utilities.default_metrics import all_numeric_metrics

def filter_similar_players(df, player_name, league_name, position, similarity_threshold, profile_match_count, max_age):
    """
    Filters players based on similarity to a selected player's metrics and age limit.

    Parameters:
        df (pd.DataFrame): DataFrame containing player data with metrics.
        player_name (str): Name of the selected player to compare others against.
        numeric_metrics (list of str): List of numeric metric columns to be compared.
        similarity_threshold (float): The similarity percentage to apply to metrics (e.g., 0.9 for 90%).
        profile_match_count (int): The minimum number of metric conditions to match to be considered similar.
        max_age (int): The maximum age limit for players to be considered in the filtered results.

    Returns:
        pd.DataFrame: DataFrame with players that match the similarity criteria.
    """
    # Extract the selected player's metrics as reference
    if league_name!='All':
        df = df[df['League'] == league_name]    
    df = df[df['Primary Position']==position]

    selected_player = df.loc[df['Name'] == player_name].iloc[0]
    
    # List to hold indices of rows that match the similarity conditions
    matching_indices = []

    # Iterate through each player in the DataFrame
    for idx, row in df.iterrows():
        # Check if the player's age is smaller than the max age
        if row['Age'] >= max_age:
            continue  # Skip this player if the age is equal to or above max_age
        
        match_count = 1  # Counter for satisfied metric conditions
        
        # Iterate over each specified metric
        for metric in all_numeric_metrics:
            # Calculate the threshold value for similarity
            threshold_value = selected_player[metric] * similarity_threshold
            
            # Check if the current player's metric meets the threshold
            if row[metric] >= threshold_value:
                match_count += 1
    
        # Check if the player meets the minimum profile match count
        if match_count >= profile_match_count:
            matching_indices.append(idx)

    # Filter the DataFrame based on matching indices
    return df.loc[matching_indices].reset_index(drop=True)
