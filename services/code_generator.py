import os
import streamlit as st
import pandas as pd
import openai

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

class CodeGenerator:
    def __init__(self):
        self.client = openai.OpenAI()
    def generate_code(self, user_query, df):
        generated = "print('code generated successfully')"
        return generated
    def execute_code(self, code):
        return "executed"
    def format_executed_code(self):
        return "format executed result"
    
