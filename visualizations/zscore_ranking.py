from scipy.stats import zscore
from utilities.default_metrics import profiles_zcore

def top_10_players_by_profile(league_name, position, profile_name, df):

    if league_name != 'All':
        df = df[df['League'] == league_name]    

    df = df[df['Minutes']>500]
    df = df[df['Primary Position'] == position]

    # Find the selected profile for the given position
    profile = next(
        (p for p in profiles_zcore.get(position, []) if p["Profile Name"] == profile_name), None
    )
    if not profile:
        raise ValueError(f"Profile '{profile_name}' for position '{position}' not found.")

    # Extract metrics and weighted metrics
    metrics = profile["Using Metrics"]
    weighted_metrics = profile["Weighted Metrics"]
    z_score_name = profile["Z Score Name"]

    # Fill missing values with the mean of each column in the selected metrics
    df[metrics] = df[metrics].apply(lambda x: x.fillna(x.mean()))
    
    # Calculate z-scores for each metric
    for metric in metrics:
        df[metric + '_z'] = zscore(df[metric])
    
    # Define weights for each metric z-score
    weights = {metric + '_z': 1.5 if metric in weighted_metrics else 1 for metric in metrics}
    
    # Initialize the profile score column to 0
    df[z_score_name] = 0
    
    # Calculate the profile score based on weighted z-scores
    for metric in metrics:
        df[z_score_name] += df[metric + '_z'] * weights[metric + '_z']

    df[z_score_name] = df[z_score_name].round(2)

    # Sort the dataframe by the calculated profile score in descending order and get the top 10
    top_10_players = df.sort_values(by=z_score_name, ascending=False).head(10).reset_index(drop=True)
    
    # Display the top 10 players with relevant columns
    return top_10_players[['Name', 'Team', 'Competition', 'Minutes', 'Primary Position', 'Age' ,z_score_name]]
