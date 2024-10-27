import streamlit as st
from utilities.utils import get_players_by_position, load_data
from visualizations.pizza_chart import create_pizza_chart
from visualizations.radar_chart import create_radar_chart
from visualizations.overall_rank import create_rank_visualization
from visualizations.scatter_plot import create_scatter_chart
from utilities.default_metrics import all_numeric_metrics

from st_pages import show_pages_from_config

DATA_PATH = 'data/All Leagues/*.csv'
show_pages_from_config()
st.set_page_config(
    page_title='Football Data Viz',
    page_icon='💹',
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('Football Player Metrics Visualization')

playing_positions = ['Centre Back', 'Full Back', 'Defensive Midfielder', 'Winger', 'Centre Forward', 'Attacking Midfielder']


with st.expander("Expand to view Pizza Chart", expanded=False):
    data_frame = load_data(DATA_PATH)
    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='pizza_positon')
    player_name = st.selectbox('Select Player:', get_players_by_position(data_frame, position), index=0, key='pizza_player')

    # Button to generate pizza chart
    if st.button('Generate Pizza Chart'):
        fig_pizza = create_pizza_chart(data_frame, player_name, position)
        if fig_pizza is not None:
            st.pyplot(fig_pizza)  # Display the pizza chart

with st.expander("Expand to view Radar Chart", expanded=False):
    data_frame = load_data(DATA_PATH)
    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='radar_positon')
    player_name = st.selectbox('Select Player:', get_players_by_position(data_frame, position), index=0, key='radar_player')

    # Button to generate pizza chart
    if st.button('Generate Radar Chart'):
        fig_radar = create_radar_chart(data_frame, player_name, position)
        if fig_radar is not None:
            st.pyplot(fig_radar)  # Display the pizza chart


with st.expander("Expand to view Scatter Plot", expanded=False):
    data_frame = load_data(DATA_PATH)
    leaguesoptions = list(data_frame['League'].unique())
    leaguesoptions.append('All')

    league = st.selectbox('Select League:',leaguesoptions[::-1], index=0, key='scatter_league')
    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='scatter_pos')

    # age_range = st.slider("Select Age Range", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), 
    #                       value=(int(df['Age'].min()), int(df['Age'].max())))


    age_range = st.slider("Select Age Range", min_value=int(18), max_value=int(50), 
                          value=(int(18), int(50)))

    minutes_range = st.slider("Select Minutes Played Range", min_value=150, 
                               max_value=int(data_frame['Minutes'].max()), 
                               value=(150, int(data_frame['Minutes'].max())))

    x_metric_display = st.selectbox(
        "Select Metric for X-Axis", 
        all_numeric_metrics,  # Use the values for the dropdown
        index=0
    )    
    # Dropdown for selecting the y-axis metric, excluding the selected x_metric
    y_metric_display = st.selectbox(
        "Select Metric for Y-Axis", 
        all_numeric_metrics,
        index=0
    )


    # Button to generate pizza chart
    if st.button(f'Generate Scatter Plot'):
        fig_scatter = create_scatter_chart(data_frame, league, position, x_metric_display, y_metric_display, age_range[0], age_range[1], minutes_range[0], minutes_range[1])
        if fig_scatter is not None:
            st.pyplot(fig_scatter)  # Display the pizza chart


with st.expander("Expand to view Player's Overall Peer Rank", expanded=False):
    data_frame = load_data(DATA_PATH)
    leaguesoptions = list(data_frame['League'].unique())
    leaguesoptions.append('All')
    league = st.selectbox('Select League:',leaguesoptions[::-1], index=0, key='overall_league')
    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='overall_position')

    # Button to generate pizza chart
    if st.button(f'Computer Ranks for {position}'):
        fig_roverall = create_rank_visualization(data_frame, league, position)
        if fig_roverall is not None:
            with st.container():
                st.write(
                    """
                    <style>
                    .dataframe th:nth-child(1) {{ width: 150px; }}  /* Width for Name */
                    .dataframe th:nth-child(2) {{ width: 100px; }}  /* Width for Team */
                    .dataframe th:nth-child(3) {{ width: 80px; }}   /* Width for Minutes */
                    .dataframe th:nth-child(4) {{ width: 120px; }}  /* Width for Overall Score */
                    .dataframe th:nth-child(5) {{ width: 10px; }}   /* Width for Overall Rank */
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.dataframe(fig_roverall, use_container_width=True)