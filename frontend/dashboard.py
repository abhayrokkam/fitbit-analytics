import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="Fitbit Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Fitbit Data Analysis")

# -------------------- URL --------------------

# Docker Compose - service URL
BACKEND_URL = "http://backend:8000" 

# -------------------- Sidebar Inputs --------------------

st.sidebar.header("Query Parameters")

# Sidebar User ID: defaults to 'synthetic'
user_id = st.sidebar.text_input("User ID", "synthetic")

# Sidebar Metric: default to 'heart_rate'
options = ['heart_rate']
metric = st.sidebar.selectbox("Choose a Metric", options=options)

# Sidebar Date: defaults to 'one week'
today = date.today()
seven_days_ago = today - timedelta(days=7)

start_date = st.sidebar.date_input("Start Date", seven_days_ago)
end_date = st.sidebar.date_input("End Date", today)

# -------------------- Fetch Data (Button Press) --------------------

if st.sidebar.button("Fetch Data"):
    if start_date > end_date:
        st.error("Error: Start date must be before end date.")
    else:
        # Construct the request URL
        request_url = f"{BACKEND_URL}/data/{user_id}/{metric}"

        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        try:
            response = requests.get(request_url, params=params)
            response.raise_for_status()

            # Process and display the data
            api_response = response.json()

            data = api_response.get('data', [])

            if data:
                df = pd.DataFrame(data)

                df['time'] = pd.to_datetime(df['time'])

                st.subheader(f"Heart Rate for {user_id}")
                st.line_chart(df, x="time", y="value")
            else:
                st.warning("No data returned from the API for the selected range.")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")