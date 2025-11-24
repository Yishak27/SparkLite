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
            
                Instructions:
1. Write Python code using pandas to answer the question.
2. Assign the final result to a variable named `result`.
3. Output ONLY the python code without any explanations.
4. Use only these libraries: pandas, matplotlib, seaborn, plotly
5. If you need to create a visualization, use plotly and assign to `fig`.
6. Format: ```python\n# your code here\n```

Important: Only output the code, no other text.

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
    def execute_code(self, code,df):
        try:
            local_vars = {
                'df': df.copy(), 
                'pd': pd,
                'plt': None,
                'seaborn': None,
                'plotly': None
            }
            import matplotlib.pyplot as plt
            import seaborn
            import plotly.express as px
            import plotly.graph_objects as go

            local_vars['plt'] = plt
            local_vars['seaborn'] = seaborn
            local_vars['px'] = px
            local_vars['go'] = go
            exec(code, {}, local_vars)
            
            # print('executed result.', local_vars)
            if 'result' in local_vars:
                result = local_vars['result']
                print('result',result)
                return result, None
            else:
                return None, "No 'result' variable found in the executed code."
            
        except Exception as e:
            print('execution code error,',e)
            return "Error on execution the code."
    def format_executed_code(self):
        return "format executed result"
    
