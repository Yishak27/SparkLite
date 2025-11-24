import os
import streamlit as st
import pandas as pd
import json
class NaturalLanguageQuery:  
    def __init__(self):
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
    
    def display_chat_interface(self):
        st.subheader("Ask Questions About Your Data")             
    