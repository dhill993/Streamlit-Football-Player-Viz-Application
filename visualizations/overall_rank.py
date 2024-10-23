
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

def get_overall_rank(data, league_name, player_name, position):
    """
    This function calculates the percentile rank for each metric column and then averages these percentiles
    to compute the overall score for each player, rounding to two decimal places.
    """
    data = data[data['Primary Position']==position]

    for metric in METRIC_COLUMNS:
        # Calculate the percentile rank for each metric and round to 2 decimal places
        data[f'{metric}_percentile'] = (data[metric].rank(pct=True) * 100).round(0)
    
    # Calculate the average of all metric percentiles to get the overall score, rounded to 2 decimal places
    data['calculated_overall_score'] = data[[f'{metric}_percentile' for metric in METRIC_COLUMNS]].mean(axis=1).round(0)
    return data[data['Name']==player_name]['calculated_overall_score'].values[0]

def create_rank_visualization(data, league_name, player_name, position):
    """
    Create an interactive horizontal bar visualization of the rank percentage.

    Parameters:
    overall_rank (float): The overall rank percentage.

    Returns:
    fig: Plotly figure object.
    """
    overall_rank = get_overall_rank(data, league_name, player_name, position)
    if overall_rank < 56:
        color = 'red'  # lower than 55%
    elif 56 <= overall_rank <= 74:
        color = 'orange'  # between 56% and 74%
    else:
        color = 'green'  # 75% and above

    # Create a horizontal bar plot
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=[overall_rank],
        y=['Overall Rank'],
        orientation='h',
        marker=dict(color=color, line=dict(color='black', width=1)),
        text=f'{overall_rank}%',
        textposition='outside',
        hovertemplate=f"<b>{player_name}</b><br>Position: {position}<br>League: {league_name}<br>Rank: {overall_rank}%<extra></extra>"
    ))

    # Update layout for aesthetics
    fig.update_layout(
        title=f'Overall Positional Rank of {player_name}',
        yaxis_title='',
        xaxis=dict(range=[0, 100]),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # No background color
        paper_bgcolor='rgba(0, 0, 0, 0)',  # No paper background color
        font=dict(color='black'),  # Font color
        margin=dict(l=40, r=40, t=40, b=40)  # Margins
    )

    return fig
