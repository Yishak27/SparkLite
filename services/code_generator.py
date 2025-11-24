import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_AI_KEY")
# print('open key',OPEN_API_KEY)

class CodeGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_API_KEY)
    def generate_code(self, user_query, df):
        try:
            prompt = f"""
            You are an expert Data Analyst.
            You have access to a pandas dataframe variable named `df`.
            The dataframe has these columns: {df}
            User Question: "{user_query}"
            Write me python code. Just the code only.
            """ 
            result = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            print('result', result)
            generated_code=  result.choices[0].message.content
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()
            print("generated code,", generated_code)
            return generated_code
        except Exception as e:
            print('error in code generation, ', e)
            return "Unable to generate code." 
    def execute_code(self, code):
        return "executed"
    def format_executed_code(self):
        return "format executed result"
    
