import streamlit as st
import pandas as pd
from utilities.default_metrics import metrics_required
import time

PASSWORD = "saqibhere"  # Replace with your desired password
st.set_page_config(
    page_title='Football Data Viz',
    page_icon='💹',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to check if required columns are present
def validate_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing columns: {', '.join(missing_columns)}")
        return False
    return True

# Streamlit layout and functionality
st.title("Upload and Replace CSV File")

st.sidebar.header("Authenticate")
password = st.sidebar.text_input("Enter Password", type="password")
# Initialize a session state variable to track whether the user has submitted a password
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if password:
    st.session_state.submitted = True  # Update session state to indicate submission

if st.session_state.submitted:

    if password == PASSWORD:

        st.write("Please upload a CSV or Excel file containing all the required columns.")
        # File uploader
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                # Check file type and read accordingly
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)

                with st.spinner("Validating Data"):
                    time.sleep(3)
                    if validate_columns(df, metrics_required):
                        # If validation passes, provide download option
                        save_path = "data/football_player_stats.csv"
                        df.to_csv(save_path, index=False)
                        st.success(f"Data updated successfully ")

            except Exception as e:
                st.error(f"Error reading file: {e}")
    else:
        st.sidebar.error("Invalid Password")
        st.warning("Please enter the correct password to proceed.")
