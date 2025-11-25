import streamlit as st
import pandas as pd
import json
from services.natural_language_service import NaturalLanguageQuery

st.set_page_config(
    page_title="SparkLite AI",
    layout="wide",
    page_icon=":search"
)

st.markdown("""
<style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 20px 0;
        margin-top: 50px;
        color: #666;
        font-size: 14px;
    }
    
    .footer a {
        color: #1f77b4;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #0d5aa7;
        text-decoration: underline;
    }
    
    .footer-brand {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
    }
    
    .footer-features {
        font-size: 12px;
        margin: 10px 0;
        color: #555;
    }
    
    .footer-copyright {
        font-size: 11px;
        color: #999;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("SparkLite AI")
st.subheader("AI agent that analyis sales data and generate a report.")

max_file_size = 20 * 1024 * 1024 

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
    
uploaded_file = st.file_uploader(
    type=["csv", "json"],
    label="Upload your data file - CSV or JSON format (Maximum size: 20MB)",
    accept_multiple_files=False,
    key="uploaded_file"
)

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
            with st.spinner("Thinking..."):
                print('user promt',user_query)
                result, generated_code = query_interface.process_user_request(user_query,st.session_state.uploaded_data)
                if result["type"] == "error":
                    response_message = "I encountered an error while analyzing the data."
                elif result["type"] == "developer_info":
                    response_message = "" 
                elif result["type"] == "unrelated_question":
                    response_message = "" 
                elif result["type"] == "chat_history":
                    response_message = ""
                else:
                    response_message = "Here's the result of my analysis:"
                # print('respons------------- last one------,', response_message, "result,", result)
                query_interface.add_assistant_response(response_message, result, generated_code)
else:
    st.info("Please upload a data file first to start asking questions.")


st.markdown("---")
st.markdown(
    """
    <div class='footer'>
        <div class='footer-brand'>SparkLite AI</div>
        <div style='margin: 10px 0;'>
            Developed by <a href='https://ermiyas.dev' target='_blank'>Ermiyas</a> | 
            Contact: <a href='mailto:inbox@ermiyas.dev'>inbox@ermiyas.dev</a>
        </div>
        <div class='footer-copyright'>
            © 2025 SparkLite AI. All rights reserved.
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)