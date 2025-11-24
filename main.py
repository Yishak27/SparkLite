import streamlit as st
import pandas as pd
import json
import io 
 
st.set_page_config(
    page_title="SparkLite AI",
    layout="wide",
    page_icon=">"
)

st.title("SparkLite AI")
st.header("This is a simple AI agent that do sales analysis.")
# df = None
max_file_size = 20 * 1024 * 1024 

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
    
uploaded_file = st.file_uploader("Upload a CSV or JSON file",type=["csv","json"],key="uploaded_file")

def display_data_profile(df):
    if df is None:
        print('no data to display')
        return
    print("in data diplay",df)
    st.subheader("Data profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows,", len(df))
    with col2:
        st.metric("Total Columns,", len(df.columns))        
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
      
try: 
    if uploaded_file is not None:
        if uploaded_file.size > max_file_size:
            st.error(f"File size is too large. Max file size is {max_file_size} bytes.")            
    if st.session_state.uploaded_data is not None:
        try:
            if st.session_state.file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                st.line_chart(df, x="product",y="id",z="yes")
            elif st.session_state.file_name.endswith(".json"):
                json_data = json.load(uploaded_file)
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
            else:
                st.error("Unsupported file format.")
            st.session_state.uploaded_data = df
            if st.session_state.uploaded_data is not None:
                print('here....')
                display_data_profile(st.session_state.uploaded_data)
        except Exception as e:
            print('erro reading file:', e)
            st.error(f"Error reading file:")
            st.session_state.uploaded_data = None
            st.session_state.file_name = None
except Exception as e:
    print('erro reading file:', e)
    st.error(f"Error reading file:")
    st.session_state.uploaded_data = None
    st.session_state.file_name = None 