import streamlit as st
import json
import pandas as pd
from io import StringIO

def flatten_json(nested_json, parent_key='', sep='.'):
    """Recursively flatten a nested JSON."""
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_json({f"{new_key}.{i}": item}, '', sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def convert_json_to_csv(flattened_data, delimiter):
    df = pd.DataFrame([flattened_data])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, sep=delimiter)
    return csv_buffer.getvalue()

# Streamlit App Layout
st.title("JSON Formatter Tool")

# Sidebar for file upload
st.sidebar.header("Upload JSON File")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type=["json"])

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("JSON Input")
    json_input = st.text_area("Paste your JSON here:", height=400)

with col2:
    st.subheader("Output")
    output_area = st.empty()

# Buttons between columns
st.sidebar.header("Actions")
if st.sidebar.button("Validate JSON"):
    try:
        if uploaded_file:
            json_data = json.load(uploaded_file)
        else:
            json_data = json.loads(json_input)
        st.sidebar.success("JSON is valid!")
        output_area.text(json.dumps(json_data, indent=4))
    except json.JSONDecodeError as e:
        st.sidebar.error(f"Invalid JSON: {e}")

delimiter = st.sidebar.text_input("CSV Delimiter", value=",")
csv_result = None  # Initialize csv_result to store the CSV data for download

if st.sidebar.button("Convert JSON to CSV"):
    try:
        if uploaded_file:
            json_data = json.load(uploaded_file)
        else:
            json_data = json.loads(json_input)
        flattened_data = flatten_json(json_data)
        csv_result = convert_json_to_csv(flattened_data, delimiter)
        st.sidebar.success("JSON converted to CSV!")
        output_area.text(csv_result)
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

if st.sidebar.button("Flatten JSON"):
    try:
        if uploaded_file:
            json_data = json.load(uploaded_file)
        else:
            json_data = json.loads(json_input)
        flattened_data = flatten_json(json_data)
        st.sidebar.success("JSON flattened!")
        output_area.text(json.dumps(flattened_data, indent=4))
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Download button for the CSV output
if csv_result:
    st.sidebar.download_button(
        label="Download CSV",
        data=csv_result,
        file_name='output.csv',
        mime='text/csv',
    )
