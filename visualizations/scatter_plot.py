import pandas as pd
import matplotlib.pyplot as plt
from utilities.utils import custom_fontt
import numpy as np

def create_scatter_chart(df, league, player, player_position, x_metric, y_metric, min_age, max_age, min_minutes, max_minutes):

    player_df = df[df["Name"] == player]
    if league != 'All':
        df = df[df['League'] == league]    
    df = df[df['Primary Position'] == player_position]
    df = df[(df['Minutes'] >= min_minutes) & (df['Minutes'] <= max_minutes)]
    df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

    if player not in df['Name'].values:
        df = pd.concat([df, player_df], ignore_index=True)

    df = df.dropna(subset=[x_metric, y_metric])
    df = df[np.isfinite(df[x_metric]) & np.isfinite(df[y_metric])]

    # Calculate percentiles
    for metric in [x_metric, y_metric]:
        df[f'{metric}_percentile'] = df[metric].rank(pct=True) * 100

    # Scatter plot for all players
    if league != 'All':
        x_percentile = 97
        y_percentile = 97
    else:
        x_percentile = 95
        y_percentile = 95

    top_x_players = df[df[f'{x_metric}_percentile'] >= x_percentile]
    top_y_players = df[df[f'{y_metric}_percentile'] >= y_percentile]
    top_both_players = df[(df[f'{x_metric}_percentile'] >= x_percentile) | (df[f'{y_metric}_percentile'] >= y_percentile)]
    top_players = pd.concat([top_x_players, top_y_players, top_both_players]).drop_duplicates()

    non_top_players = df[~df['Name'].isin(top_players['Name'])]
    random_players = non_top_players.sample(15)

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(16,10), facecolor='#222222')
    ax.set_facecolor('#222222')

    ax.scatter(df[x_metric], df[y_metric], 
               alpha=0.25, c='#83bd8e', edgecolor='black', s=120, marker='o', label='Players')

    # Highlight top performers
    ax.scatter(top_players[x_metric], top_players[y_metric], 
               c='#358244', s=180, marker='o', edgecolor='grey', label='Top Performers', alpha=0.6)

    # Check if the player is in top_players to avoid duplicate highlighting
    player_row = df[df['Name'] == player]
    if not player_row.empty:
        if player in top_players['Name'].values:
            # Remove the player from top_players to avoid duplicate styling
            top_players = top_players[top_players['Name'] != player]

        # Highlight selected player with red color
        ax.scatter(player_row[x_metric], player_row[y_metric], 
                   c='red', s=180, marker='o', edgecolor='black', label=player, alpha=0.4)
        ax.annotate(
            player, 
            (player_row[x_metric].values[0], player_row[y_metric].values[0]),
            fontsize=8, color='white', ha='left', va='bottom', fontproperties=custom_fontt, alpha=0.9
        )

    # Annotate remaining top players
    for _, row in top_players.iterrows():
        name_parts = row['Name'].split()
        initials = f"{name_parts[0][0]}. {name_parts[-1]}" if len(name_parts) > 1 else name_parts[0]
        ax.annotate(
            initials,
            (row[x_metric], row[y_metric]),
            fontsize=8, color='#d0ceda', alpha=0.7, ha='left', va='bottom', fontproperties=custom_fontt
        )

    # Annotate random players' names
    for _, row in random_players.iterrows():
        ax.annotate(
            row['Name'],
            (row[x_metric], row[y_metric]),
            fontsize=8, color='white', ha='left', va='top', fontproperties=custom_fontt, alpha=0.6
        )

    # Titles and labels
    plt.title(f'{y_metric}  vs.  {x_metric}\n', fontproperties=custom_fontt, ha='center', color='white', fontsize=20)
    plt.xlabel(x_metric, fontsize=12, fontproperties=custom_fontt, color='white')
    plt.ylabel(y_metric, fontsize=12, fontproperties=custom_fontt, color='white')

    # Set white color for axis lines and tick labels
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    avg_x = df[x_metric].mean()
    avg_y = df[y_metric].mean()
    ax.axhline(y=avg_y, color='white', linestyle=':', linewidth=1, label=f'Average {y_metric}')
    ax.axvline(x=avg_x, color='white', linestyle=':', linewidth=1, label=f'Average {x_metric}')
    
    x_lim = list(map(abs, ax.get_xlim()))
    y_lim = list(map(abs, ax.get_ylim()))

    ax.text(x_lim[1] * 0.95, y_lim[1] * 0.95, f'High {x_metric}, High {y_metric}', color='green', fontsize=9, ha='right', va='top')
    ax.text(x_lim[1] * 0.95, y_lim[0], f'High {x_metric}, Low {y_metric}', color='green', fontsize=9, ha='right', va='bottom')
    ax.text(x_lim[0], y_lim[1] * 0.95, f'Low {x_metric}, High {y_metric}', color='green', fontsize=9, ha='left', va='top')
    ax.text(x_lim[0], y_lim[0], f'Low {x_metric}, Low {y_metric}', color='green', fontsize=9, ha='left', va='bottom')

    footer_text = (f"Chosen Leagues :- {league}\n"
                   f"Chosen Position :- {player_position}\n")
    plt.text(0, -0.125, footer_text, ha='left', fontproperties=custom_fontt, fontsize=10, color='white', 
             alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')

    footer_text2 = (f"Age Range :- {min_age} - {max_age}\n"
                    f"Minutes Range :- {min_minutes} - {max_minutes}\n")
    plt.text(1, -0.125, footer_text2, ha='right', fontproperties=custom_fontt, fontsize=10, color='white',
             alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')

    # Return the figure object
    return fig
