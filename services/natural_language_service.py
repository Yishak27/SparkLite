import os
import streamlit as st
import pandas as pd
from .code_generator import CodeGenerator

class NaturalLanguageQuery:  
    def __init__(self):
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
    
    def display_chat_interface(self):
        st.subheader("Ask Questions About Your Data")     
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    def process_user_request(self, user_query,df):
        try:
            code_generation = CodeGenerator

            with st.spinner("generating analysis code"):
                generated = code_generation.generate_code(self,user_query,df)
                print("generated", generated)
            with st.expander:
                st.code(generated)
            return 
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
    
    def add_assistant_response(self, response):
        st.session_state.chat_messages.append({"role": "assistant", "content": response})        
        with st.chat_message("assistant"):
            st.write(response)

