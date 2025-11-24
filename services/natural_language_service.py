import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
from .code_generator import CodeGenerator

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_AI_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
print('open key',OPEN_API_KEY, GROK_API_KEY)
class NaturalLanguageQuery:  
    def __init__(self):
        # self.client = openai.OpenAI(api_key=OPEN_API_KEY)
        self.client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROK_API_KEY
        )
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
            # with st.spinner("generating analysis code"):
            generated = code_generation.generate_code(self,user_query,df)
            print("generated", generated)
            with st.expander("View Generated Code"):
                st.code(generated, language="python")
            return generated
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

