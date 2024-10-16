import pandas as pd 
import streamlit as st
from mplsoccer import PyPizza
from matplotlib.patches import Patch,Circle
from PIL import Image
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# Font paths
font_path = "fonts/Rajdhani-Bold.ttf"
font_pathh = "fonts/Alexandria-Regular.ttf"
font_pathhh = "fonts/Alexandria-SemiBold.ttf"

# Load the font using FontProperties
custom_font = fm.FontProperties(fname=font_path)
custom_fontt = fm.FontProperties(fname=font_pathh)
custom_fonttt = fm.FontProperties(fname=font_pathhh)


# Load the data from CSV
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Helper function to get players by position
def get_players_by_position(df, position):
    return df[df['Primary Position'] == position]['Name'].tolist()

# Helper function to get player metrics
def get_player_metrics(df, player_name):
    player_data = df[df['Name'] == player_name]
    if not player_data.empty:
        return player_data
    return None

def create_pizza_chart(complete_data, player_name):
    # Get player metrics
    player_df = get_player_metrics(complete_data, player_name)
    
    if player_df is None or player_df.empty:
        st.error(f'Player {player_name} not found.')
        return None

    # Define the categories and metrics
    categories = {
        "Defensive": ["Dribbles Stopped%", "Aerial Win%", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["OP F3 Pass", "Carry Length", "xGBuildup"],
        "Advanced": ["PAdj Clearances", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    }

    # Merge all categories' metrics into one list (to match the DataFrame columns)
    all_metrics = sum(categories.values(), [])

    # Check for available metrics
    available_metrics = [metric for metric in all_metrics if metric in player_df.columns]

    if not available_metrics:
        st.error("No valid metrics found for this player.")
        return None

    # Extract the player metric values from the DataFrame for available metrics
    metric_values = player_df[available_metrics].iloc[0].values.tolist()

    # Ensure that metrics and values match
    if len(available_metrics) != len(metric_values):
        st.error("Metric mismatch error.")
        return None

    # Assign colors to each category
    category_colors = {
        "Defensive": "#1A78CF",
        "Progressive": "#58AC4E",
        "Advanced": "#aa42af"
    }

    # Assign slice colors based on the metric's category
    slice_colors = []
    for metric in available_metrics:
        for category, metrics in categories.items():
            if metric in metrics:
                slice_colors.append(category_colors[category])

    baker = PyPizza(
        params=available_metrics,                  # list of parameters
        background_color="#222222",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=4,               # linewidth for last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    fig, ax = baker.make_pizza(
        metric_values,
        figsize=(9.5, 11),
        color_blank_space="same",
        blank_alpha=0.1,
        slice_colors=slice_colors,
        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=2),
        kwargs_params=dict(color="#F2F2F2", fontsize=12, fontproperties=fm.FontProperties(fname=font_pathh), va="center"),
        kwargs_values=dict(color="#F2F2F2", fontsize=0, alpha=0, fontproperties=fm.FontProperties(fname=font_pathh), zorder=-5)
    )
    # # Initialize PyPizza
    # baker = PyPizza(
    #     params=available_metrics,             
    #     background_color="#222222",           
    #     straight_line_color="#000000",        
    #     straight_line_lw=2,                   
    #     last_circle_lw=2,                     
    #     other_circle_lw=0,                    
    #     inner_circle_size=10                   
    # )

    # # Plot pizza chart
    # fig, ax = baker.make_pizza(
    #     metric_values,                        
    #     figsize=(10, 10),                     
    #     color_blank_space="same",             
    #     slice_colors=slice_colors,            
    #     value_bck_colors=["#111111"] * len(available_metrics),  
    #     blank_alpha=0.4,                     
    #     kwargs_slices=dict(edgecolor="#FFFFFF", linewidth=2),  
    #     kwargs_params=dict(color="#FFFFFF", fontsize=12, va="center")  
    # )


    # Create custom legend
    legend_elements = [
        Patch(facecolor=category_colors["Defensive"], edgecolor='white', label='Defensive'),
        Patch(facecolor=category_colors["Progressive"], edgecolor='white', label='Progressive'),
        Patch(facecolor=category_colors["Advanced"], edgecolor='white', label='Advanced')
    ]


            # Retrieve Minutes Played and Age from the player data
    position = player_df['Primary Position']  # Assuming 'Age' exists

    fig.text(
        0.08, 0.94, f"{player_name}", size=25,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2"
    )

    fig.text(
        0.08, 0.92,
        "Percentile Rank vs. Positional Peers | Stats per 90",
        size=10,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    # Convert 'Minutes Played' to an integer to remove decimals
    minutes_played = int(player_df['Minutes'])

    fig.text(
        0.08, 0.90,
        f"Minutes Played: {minutes_played} | Age: {int(player_df['Age'])}",
        size=10,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    # Add a horizontal line at the top with the team's primary color
    fig.add_artist(plt.Line2D((0, 1.2), (0.88, 0.88), color='white', linewidth=2, alpha=0.8, transform=fig.transFigure))

    # Add the legend to the figure (bottom-right corner)
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=12, frameon=False, labelcolor='white')
       
    # Coordinates for the circles
    circle1_center_x, circle1_center_y = 0.5, 0.5  # Circle 1 center
    circle2_center_x, circle2_center_y = 0.5, 0.5  # Circle 2 center
    circle3_center_x, circle3_center_y = 0.5, 0.5  # Circle 3 center
    circle4_center_x, circle4_center_y = 0.5, 0.5  # Circle 4 center
    
    # Add circles
    circle_params = [
        (0.415, circle1_center_x, circle1_center_y),  # Circle 1
        (0.330, circle2_center_x, circle2_center_y),  # Circle 2
        (0.245, circle3_center_x, circle3_center_y),  # Circle 3
        (0.160, circle4_center_x, circle4_center_y)   # Circle 4
    ]
    
    for radius, x, y in circle_params:
        circle = Circle((x, y), radius, color='black', alpha=0.25, fill=False, zorder=50, linewidth=1.75, transform=ax.transAxes)
        ax.add_patch(circle)
    
    # Add text above circles
    # Add text '80' above circle 1
    ax.text(circle1_center_x, circle1_center_y + 0.395, '80',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '60' above circle 2
    ax.text(circle2_center_x, circle2_center_y + 0.31, '60',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '40' above circle 3
    ax.text(circle3_center_x, circle3_center_y + 0.225, '40',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '20' above circle 4
    ax.text(circle4_center_x, circle4_center_y + 0.14, '20',
            ha='center', va='center', fontsize=13, zorder=80, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Load the image
    logo_image = Image.open('scout.png')
    
    # Coordinates for the top right corner
    logo_ax = fig.add_axes([0.4421, 0.427, 0.1375, 0.1375])
    
    # Display the image with reduced transparency
    logo_ax.imshow(logo_image, alpha=0.05)  # Set alpha to 0.1 (adjust as needed)
    
    # Hide the axis
    logo_ax.axis('off')

    return fig


file_path = 'football_player_stats.csv'

# Load the data
df = load_data(file_path)

# Streamlit UI
st.title('Football Player Metrics Visualization')

# Dropdown for selecting player position
# position = st.selectbox('Select Playing Position:', [df['Primary Position'].unique()], index=None)
position = st.selectbox('Select Playing Position:', ['Centre Back'], index=None)

# Filter players by selected position
players = get_players_by_position(df, position)
player_name = st.selectbox('Select Player:', players, index=None)

# Button to generate pizza chart
if st.button('Generate Pizza Chart'):
    fig_pizza = create_pizza_chart(df, player_name)
    if fig_pizza is not None:
        st.pyplot(fig_pizza)  # Display the pizza chart
