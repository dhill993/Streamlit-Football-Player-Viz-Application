
import pandas as pd
from utilities.default_metrics import all_numeric_metrics

def get_overall_rank(data, league_name, position):
    """
    This function calculates the percentile rank for each metric column and then averages these percentiles
    to compute the overall score for each player, rounding to two decimal places.
    """
    if league_name!='All':
        data = data[data['League'] == league_name]    
    data = data[data['Primary Position']==position]
    data = data[data['Minutes']>=500]
    data['Age'] = data['Age'].astype(int)

    for metric in all_numeric_metrics:
        # Calculate the percentile rank for each metric and round to 2 decimal places
        data[f'{metric}_percentile'] = (data[metric].rank(pct=True) * 100).round(0)

    # Calculate the average of all metric percentiles to get the overall score, rounded to 2 decimal places
    data['Overall Score'] = data[[f'{metric}_percentile' for metric in all_numeric_metrics]].mean(axis=1)

    data = data.sort_values(by='Overall Score', ascending=False)
    return data[['Name', 'Team', 'Age', 'Minutes', 'Overall Score']]

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
    overall_rank_df['Overall Score'] = pd.to_numeric(overall_rank_df['Overall Score'], errors='coerce')
    overall_rank_df['Overall Score'] = overall_rank_df['Overall Score'].apply(lambda x: round(x, 2))
    overall_rank_df = overall_rank_df.reset_index()
    overall_rank_df.index = overall_rank_df.index + 1  # Start the index from 1

    styled_df = overall_rank_df[['Name', 'Team', 'Age', 'Minutes', 'Overall Score']].style \
        .format({"Overall Score": "{:.2f}"}) \
        .apply(color_overall_score, axis=1, subset=['Overall Score'])

    return styled_df
