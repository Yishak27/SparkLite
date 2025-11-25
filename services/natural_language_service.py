import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
from .code_generator import CodeGenerator
from .visualization import AutoVisualization

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_AI_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_KEYS = [k.strip() for k in GROK_API_KEY.split(",") if k.strip()]

class NaturalLanguageQuery:  
    def __init__(self):
         if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
            
    def display_chat_interface(self):
        st.subheader("Ask Questions About Your Data")     
        if st.session_state.chat_messages is not None:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])


    def get_dataframe_info(self, df):
        columns_info = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            columns_info.append(f"{col} ({dtype})")
        return ", ".join(columns_info)

    def process_user_request(self, user_query,df):
        try:
            code_generation = CodeGenerator
            df_info = self.get_dataframe_info(df)
            # with st.spinner("generating analysis code"):
            generated = code_generation.generate_code(self,user_query,df_info)
            # print("generated", generated)
            with st.expander("View Generated Code"):
                st.code(generated, language="python")
            with st.spinner("Executing analysis..."):
                result, error = code_generation.execute_code(self,generated, df)
                # print('code execution,', result, error)
            formatted_result = code_generation.format_executed_code(self,result, error)
            # print('formatttttt.........', formatted_result)
            return formatted_result,generated
        except Exception as e:
            print("error occur",e)

    def get_user_query(self):
        user_query = st.chat_input("Ask a question about your data...")        
        if user_query:
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)            
            return user_query
        return None
    
    def add_assistant_response(self,response,result_data):
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            if result_data:
                st.write(result_data["display"])                
                if result_data["type"] == "dataframe":
                    st.dataframe(result_data["content"])
                elif result_data["type"] == "error":
                    st.error(result_data["content"])
                elif result_data["type"] in ["number", "text", "unknown"]:
                    st.info(result_data["content"])

                if result_data.get("visualization"):
                    st.subheader("Visualized Data")
                    st.plotly_chart(result_data["visualization"], width='content')
                    st.caption("Automatic visualization generated based on your data")
