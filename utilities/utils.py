import pandas as pd
import matplotlib.font_manager as fm

custom_fontt = fm.FontProperties(fname="fonts/Alexandria-Regular.ttf")


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
