import pandas as pd
import matplotlib.pyplot as plt
from utilities.utils import custom_fontt


def create_scatter_chart(df, league, player_position, x_metric, y_metric, min_age, max_age, min_minutes, max_minutes):

    df = df[df['Primary Position']==player_position]
    df = df[(df['Minutes'] >= min_minutes) & (df['Minutes'] <= max_minutes)]
    # df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

    # Calculate percentiles
    for metric in [x_metric, y_metric]:
        df[f'{metric}_percentile'] = df[metric].rank(pct=True) * 100

    # Filter based on percentiles
    x_percentile = 95  # Adjust as needed
    y_percentile = 95  # Adjust as needed
    top_x_players = df[df[f'{x_metric}_percentile'] >= x_percentile]
    top_y_players = df[df[f'{y_metric}_percentile'] >= y_percentile]
    top_both_players = df[(df[f'{x_metric}_percentile'] >= x_percentile) & (df[f'{y_metric}_percentile'] >= y_percentile)]
    
    top_players = pd.concat([top_x_players, top_y_players, top_both_players]).drop_duplicates()

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#222222')
    ax.set_facecolor('#222222')
    
    # Scatter plot for all players
    valid_data = df.dropna(subset=[x_metric, y_metric])
    ax.scatter(valid_data[x_metric], valid_data[y_metric], 
               alpha=0.25, c='#83bd8e', edgecolor='black', s=120, marker='o', label='Players')

    # Annotated players
    ax.scatter(top_players[x_metric], top_players[y_metric], 
               c='#358244', s=175, marker='o', edgecolor='grey', label='Top Performers', alpha=0.6)

    # Annotate names
    for _, row in top_players.iterrows():
        ax.annotate(row['Name'], (row[x_metric], row[y_metric]),
                    fontsize=11, color='#d0ceda', alpha=1, ha='center', fontproperties=custom_fontt)

    # Titles and labels
    plt.title(f'{y_metric}  vs.  {x_metric}\n', fontproperties=custom_fontt, ha='center', color='white', fontsize=20)

    plt.xlabel(x_metric, fontsize=12, fontproperties=custom_fontt, color='white')
    plt.ylabel(y_metric, fontsize=12, fontproperties=custom_fontt, color='white')

    # Show grid
    plt.grid(color='gray', linestyle='--', linewidth=0.25)
        # Create the footer text
    footer_text = (f"Chosen Leagues :- {league}\n"
                    f"Chosen Position :- {player_position}\n")

    # Add footer text to the plot
    plt.text(0, -0.125, footer_text, ha='left', fontproperties=custom_fontt, fontsize=10, color='white', 
                alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')


    # Create a formatted string for the footer
    footer_text2 = (f"Age Range :- {max_age} - {min_age}\n"
                        f"Minutes Range :- {min_minutes} - {max_minutes}\n")

    # Add footer text to the plot
    plt.text(1, -0.125, footer_text2, ha='right', fontproperties=custom_fontt, fontsize=10, color='white',
                alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')

    # Return the figure object
    return fig

