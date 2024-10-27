import streamlit as st
import pandas as pd
import os
import shutil
from utilities.default_metrics import metrics_required
import time

PASSWORD = "saqibhere"  # Replace with your desired password

st.set_page_config(
    page_title='Bristol Rovers - Data Analysis Tool',
    page_icon='💹',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Directory to save updated files
data_dir = "data/All Leagues"

# Function to check if required columns are present
def validate_columns(df, required_columns, file_name):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"File {file_name} is missing these required columns: {', '.join(missing_columns)}")
        return False
    return True

# Function to clear existing files in the data directory
def clear_data_folder():
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)

# Streamlit layout and functionality
st.title("Update Player's Data")

st.sidebar.header("Authenticate")
password = st.sidebar.text_input("Enter Password", type="password")

# Initialize session state for authentication
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if password:
    st.session_state.submitted = True

if st.session_state.submitted:

    if password == PASSWORD:
        st.write("Please upload CSV or Excel files containing all the required metrics.")
        
        # File uploader for multiple files
        uploaded_files = st.file_uploader("Choose CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

        if uploaded_files:
            valid_files = []
            for uploaded_file in uploaded_files:
                try:
                    # Check file type and read accordingly
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith('.xlsx'):
                        df = pd.read_excel(uploaded_file)

                    with st.spinner(f"Validating {uploaded_file.name}..."):
                        time.sleep(1)
                        if validate_columns(df, metrics_required, uploaded_file.name):
                            valid_files.append((uploaded_file.name, df))

                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {e}")

            # Update data if files are valid
            if valid_files:
                if st.button("Update Data")  :
                    clear_data_folder()
                    for file_name, df in valid_files:
                        save_path = os.path.join(data_dir, f"{os.path.splitext(file_name)[0]}.csv")
                        df.to_csv(save_path, index=False)
                        st.success(f"File {file_name} have been saved successfully.")
    else:
        st.sidebar.error("Invalid Password")
        st.warning("Please enter the correct password to proceed.")
