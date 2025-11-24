import streamlit as st
import pandas as pd
import json
from services.natural_language_service import NaturalLanguageQuery

st.set_page_config(
    page_title="SparkLite AI",
    layout="wide",
    page_icon=">"
)

st.title("SparkLite AI")
st.header("This is a simple AI agent that do sales analysis.")

max_file_size = 20 * 1024 * 1024 

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

uploaded_file = st.file_uploader("Upload a CSV or JSON file", type=["csv","json"], key="uploaded_file")

def display_data_profile(df):
    if df is None:
        return
    st.subheader("Data profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))        
    st.write("**First 5 Rows:**")
    st.dataframe(df.head())
    
    st.write("**Column Information:**")
    column_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(column_info)

if uploaded_file is not None:
    if uploaded_file.size > max_file_size:
        st.error(f"File size is too large. Max file size is {max_file_size // (1024*1024)}MB.")
    else:
        try:
            st.session_state.file_name = uploaded_file.name
            
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                uploaded_file.seek(0)
                json_data = json.load(uploaded_file)
                if isinstance(json_data, list):
                    df = pd.DataFrame(json_data)
                elif isinstance(json_data, dict):
                    if 'data' in json_data and isinstance(json_data['data'], list):
                        df = pd.DataFrame(json_data['data'])
                    else:
                        df = pd.DataFrame([json_data])
                else:
                    st.error("Unsupported JSON structure")
                    df = None
            
            if df is not None:
                st.session_state.uploaded_data = df
                st.success(f"File uploaded successfully: {uploaded_file.name}")
                display_data_profile(df)
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.session_state.uploaded_data = None
            st.session_state.file_name = None

if st.session_state.uploaded_data is not None:
    query_interface = NaturalLanguageQuery() 
    query_interface.display_chat_interface()
    user_query = query_interface.get_user_query()
    
    if user_query:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                placeholder_response = "AI response for the give question will be done here...."
                query_interface.add_assistant_response(placeholder_response)
else:
    st.info("Please upload a data file first to start asking questions.")