import streamlit as st
import pandas as pd
import json
import io 
 
max_file_size = 20 * 1024 * 1024 
st.title("SparkLite AI")
st.header("This is a simple AI agent that do sales analysis.")
df = None
st.set_page_config(
    page_title="SparkLite AI",
    layout="wide",
    page_icon=">"
)

if 'uploaded_data' not in st.session_state or 'file_name' not in st.session_state:
    st.session_state.uploaded_data = None
    st.session_state.file_name = None
uploaded_file = st.file_uploader(
    "Upload a CSV or JSON file",
    help=None,
    type=["csv","json"],
    key="uploaded_file"
)
try: 
    if uploaded_file is not None:
        if uploaded_file.size > max_file_size:
            st.error(f"File size is too large. Max file size is {max_file_size} bytes.")            
    if st.session_state.uploaded_data is not None:
        try:
            if st.session_state.file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif st.session_state.file_name.endswith(".json"):
                if isinstance(json_data, list):
                    df = pd.DataFrame(json_data)
                elif isinstance(json_data, dict):
                    print('readed data, ', json_data)
                    if 'data' in json_data and isinstance(json_data['data'], list):
                        df = pd.DataFrame(json_data['data'])
                    else:
                        df = pd.DataFrame([json_data])
                else:
                    st.error("Unsupported JSON structure")
                    df = None
                st.session_state.uploaded_data = df
            else:
                st.error("Unsupported file format.")
            
        except Exception as e:
            print('erro reading file:', e)
            st.error(f"Error reading file:")
            st.session_state.uploaded_data = None
            st.session_state.file_name = None
    if df is not None:
        st.line_chart(df, x="product", y="total_price") 
except Exception as e:
    print('erro reading file:', e)
    st.error(f"Error reading file:")
    st.session_state.uploaded_data = None
    st.session_state.file_name = None  