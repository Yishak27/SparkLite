import streamlit as st
import time
class LoaderComponent:
    def show_thinking_loader(self, message="Thinking...."):
        with st.chat_message("assistant"):
            with st.status(message, expanded=True) as status:
                st.write("Analyzing your question...")
                st.write("Understanding the data structure...")
                st.write("Generating analysis code...")
                time.sleep(1)
            return status