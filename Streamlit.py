import streamlit as st
import json
import pandas as pd
from io import StringIO

# Title and description
st.title("JSON to CSV Tool")
st.write("A simple web application for formatting, validating, and converting JSON data.")

# Layout with two columns
col1, col2 = st.columns(2)

# Input area for JSON   data
with col1:
    st.subheader("Input JSON")
    json_input = st.text_area("Paste your JSON here", height=300)

# Output area for results
with col2:
    st.subheader("Output")
    result_area = st.empty()

# Buttons in between columns
st.subheader("Actions")

# File uploader
uploaded_file = st.file_uploader("Upload a JSON file", type="json")
if uploaded_file:
    try:
        json_input = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Failed to read file: {e}")

# Validate JSON
if st.button("Validate JSON"):
    try:
        parsed_json = json.loads(json_input)
        result_area.json(parsed_json)
        st.success("JSON is valid!")
    except json.JSONDecodeError as e:
        result_area.error("Invalid JSON")
        st.error(f"JSON validation failed: {e}")

# Convert JSON to CSV
if st.button("Convert JSON to CSV"):
    try:
        parsed_json = json.loads(json_input)

        # Handle nested JSON and JSON arrays
        if isinstance(parsed_json, list):
            df = pd.json_normalize(parsed_json)
        elif isinstance(parsed_json, dict):
            df = pd.json_normalize([parsed_json])
        else:
            st.error("Unsupported JSON format. Must be an object or array.")
            st.stop()

        # Select delimiter
        delimiter = st.text_input("Enter a delimiter for the CSV file (default is ','):", value=",")
        if len(delimiter) != 1:
            st.error("Delimiter must be a single character.")
        else:
            csv_data = StringIO()
            df.to_csv(csv_data, index=False, sep=delimiter)
            csv_data.seek(0)

            result_area.text(csv_data.getvalue())

            # Download link
            st.download_button(
                label="Download CSV",
                data=csv_data.getvalue(),
                file_name="converted_file.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
