
import plotly.graph_objects as go

METRIC_COLUMNS = [
    "NP Goals", "xG", "xG/Shot", "Shots", "Shooting%", 
    "Shot Touch%", "Assists", "xG Assisted", "Key Passes", 
    "Scoring Contribution", "Dribbles", "Successful Dribbles", 
    "Dispossessed", "PAdj Interceptions", "PAdj Clearances", 
    "Defensive Actions", "Aggressive Actions", "Blocks/Shot", 
    "Defensive Regains", "Ball Recov. F2", "Ball Recoveries", 
    "PAdj Tackles", "Dribbles Stopped%", "Aerial Win%", 
    "Passing%", "Long Ball%", "xGBuildup", "Carry Length", 
    "OP F3 Passes", "PinTin", "Successful Crosses", "Crossing%"
]

def get_overall_rank(data, league_name, position):
    """
    This function calculates the percentile rank for each metric column and then averages these percentiles
    to compute the overall score for each player, rounding to two decimal places.
    """
    data = data[data['Primary Position']==position]
    data = data[data['Minutes']>=500]

    for metric in METRIC_COLUMNS:
        # Calculate the percentile rank for each metric and round to 2 decimal places
        data[f'{metric}_percentile'] = (data[metric].rank(pct=True) * 100).round(0)
    
    # Calculate the average of all metric percentiles to get the overall score, rounded to 2 decimal places
    data['Overall Score'] = data[[f'{metric}_percentile' for metric in METRIC_COLUMNS]].mean(axis=1).astype(int)
    data = data.sort_values(by='Overall Score', ascending=False)
    return data[['Name', 'Team', 'Minutes', 'Overall Score']]

def create_rank_visualization(data, league_name, position):
    """
    Create an interactive horizontal bar visualization of the rank percentage.

    Parameters:
    overall_rank (float): The overall rank percentage.

    Returns:
    fig: Plotly figure object.
    """
    def color_overall_score(row):
        overall_score = row['Overall Score']
        if overall_score < 50 :
            return ['background-color: red']  # lower than 55%
        elif 50 <= overall_score <= 69:
            return ['background-color: orange']  # between 56% and 74%
        else:
            return ['background-color: green']  # 75% and above

    overall_rank_df = get_overall_rank(data, league_name, position)
    overall_rank_df = overall_rank_df.reset_index()
    overall_rank_df.index = overall_rank_df.index + 1  # Start the index from 1

    styled_df = overall_rank_df[['Name', 'Team', 'Minutes', 'Overall Score']].style.apply(color_overall_score, axis=1, subset=['Overall Score'])

    return styled_df
