import streamlit as st
import pandas as pd
import json
 
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
st.file_uploader("Upload a CSV file", type="csv,json", key="uploaded_file")
if st.session_state.uploaded_file is not None:
    st.session_state.uploaded_data = st.session_state.uploaded_file.read()
    st.session_state.file_name = st.session_state.uploaded_file.name

st.write("file uploaded", st.session_state.file_name)
st.write("file data", st.session_state.uploaded_data)
if st.session_state.uploaded_data is not None:
    df = pd.read_csv(st.session_state.uploaded_data)
    st.line_chart(df, x="product", y="total_price")