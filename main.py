import streamlit as st
import pandas as pd
import json
import io 
 
st.title("SparkLite AI")
st.header("This is a simple AI agent that do sales analysis.")

st.set_page_config(
    page_title="SparkLite AI",
    layout="wide",
    page_icon=">"
)

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv","json"], key="uploaded_file")
if uploaded_file is not None:
    st.session_state.uploaded_data = uploaded_file.read()
    st.session_state.file_name = uploaded_file.name

st.write("file uploaded", st.session_state.file_name)
# st.write("file data", st.session_state.uploaded_data)
if st.session_state.uploaded_data is not None:
    try:
        df = pd.read_csv(io.BytesIO(st.session_state.uploaded_data))
    except Exception as e:
        st.error(f"Error reading file: {e}")
    st.line_chart(df, x="product", y="total_price")