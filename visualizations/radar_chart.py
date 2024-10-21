import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.patches import Patch
from utilities.default_metrics import all_metric_categories
from utilities.utils import get_player_and_avg_metrics, get_stat_values
from utilities.utils import custom_fontt



def create_radar_chart(complete_data, player_name, position):
    player_data = complete_data[complete_data['Name'] == player_name]
    player_metrics_df, positional_means_df = get_player_and_avg_metrics(complete_data, player_name, position)

    position_specific_categories = all_metric_categories[position]
    keys_list = list(position_specific_categories.keys())
    all_metrics = sum(position_specific_categories.values(), [])
    metric_categories_list = []
    for metric in all_metrics:
        for category, metrics in position_specific_categories.items():
            if metric in metrics:
                metric_categories_list.append(category)

    stats1, stats2 = get_stat_values(all_metrics, player_metrics_df, positional_means_df)

    category_colors = {
        keys_list[0]: "#01e0e1",
        keys_list[1]: "#c49c3a",
        keys_list[2]: "#fa6697"
    }

    num_vars = len(all_metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles = [(angle + np.pi / 2) % (2 * np.pi) for angle in angles]
    angles = angles[::-1]  # Reverse the order for clockwise plotting

    # Close the loop by adding the first angle to the end for closing the chart
    angles += angles[:1]  
    stats1 += stats1[:1]  # Close the stats1 loop
    stats2 += stats2[:1]  # Close the stats2 loop
    
    fig1, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    fig1.patch.set_facecolor('#2E2E2A')  # Dark background for the figure
    ax.set_facecolor('#2E2E2A')  # Dark background for the plot area
    ax.spines['polar'].set_visible(True)  # Ensure the outer circle (spine) is visible
    ax.spines['polar'].set_edgecolor('grey')  # Set the outer circle color to white
    ax.spines['polar'].set_linewidth(1)  # Increase the line width for better visibility
    y_ticks = [20, 40, 60, 80]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks, color='grey', size=10)
    ax.set_ylim(0, 100)  # Set the limit of y-axis to 0-100
    ax.yaxis.grid(True, color='grey', linestyle='dashed')
    ax.plot(angles, stats1, color='#1f77b4', linewidth=2, linestyle='solid')
    ax.fill(angles, stats1, color='#1f77b4', alpha=0.25)
    ax.plot(angles, stats2, color='#d62728', linewidth=2, linestyle='solid')
    ax.fill(angles, stats2, color='#d62728', alpha=0.25)

    # Draw circles at specified intervals (20, 40, 60, 80, and a max circle for 100)
    for tick in [20, 40, 60, 80]:
        circle = plt.Circle((0, 0), tick / 100 * 1.1, color='white', fill=False, linestyle='dotted', linewidth=1.5)
        ax.add_artist(circle)
    
    max_circle = plt.Circle((0, 0), 1.1, color='white', fill=False, linestyle='dotted', linewidth=2, zorder=10)
    ax.add_artist(max_circle)


    
    # Rotate and place each label using the category color
    for angle, label, category in zip(angles[:-1], all_metrics, metric_categories_list):
        # Calculate rotation
        rotation = angle * 180 / np.pi - 90  # Convert radians to degrees and adjust
        if angle > np.pi:  # Check if the angle is greater than 180 degrees
            rotation += 180  # Flip the rotation by adding 180 degrees
        color = category_colors.get(category, 'white')  # Default to black if category not found
        ax.text(angle, 105, label, ha='center', va='center', rotation=rotation, 
                rotation_mode='anchor', color=color, fontsize=12, fontproperties=custom_fontt)

    # Remove angle labels
    ax.set_xticks([])  # Hides the angle labels

    # Title and legend
    ax.text(-0.15, 1.19, "Radar Comparison Chart", ha='left', va='center', 
            fontproperties=custom_fontt, fontsize=25, color='white', transform=ax.transAxes)

    ax.text(1.3, 1.17, f"{player_name}\n{player_data.iloc[0]['Team']} Club\n{int(player_data.iloc[0]['Minutes'])} Min.", ha='right', va='center', 
            fontproperties=custom_fontt, fontsize=14, color='#1f77b4', alpha=0.8, transform=ax.transAxes)

    ax.text(-0.15, 1.14, "Players' Metrics vs Mean Positional Peers", 
            ha='left', va='center', fontproperties=custom_fontt, fontsize=12, color='white', alpha=0.5, transform=ax.transAxes)

    # Add a horizontal line at the top
    fig1.add_artist(plt.Line2D((0, 1.2), (0.935, 0.935), color='white', linewidth=2.5, alpha=0.8, transform=fig1.transFigure))

    # Create legend
    # Create custom legend
    legend_elements = [
        Patch(facecolor=category_colors[keys_list[0]], edgecolor='white', label=keys_list[0]),
        Patch(facecolor=category_colors[keys_list[1]], edgecolor='white', label=keys_list[1]),
        Patch(facecolor=category_colors[keys_list[2]], edgecolor='white', label=keys_list[2])
    ]
    
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=12, frameon=False, labelcolor='white')

    return fig1
