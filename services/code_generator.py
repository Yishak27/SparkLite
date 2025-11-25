import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
from .ai_generator  import AICodeGenarator
from .visualization import AutoVisualization
from .ai_naration import NarationSummary

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_AI_KEY")

class CodeGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_API_KEY)
        
    def generate_code(self, user_query, df):
        return self.generate_code_with_context(user_query, df, {})
    
    def generate_code_with_context(self, user_query, df, context=None):
        ais = AICodeGenarator()
        try:
            # Build context-aware prompt
            # if the prompt is not about the sales, like developer information, use this data
            developerInfo = {
                "name":"Ermiyas Developer",
                "website":"https://ermiyas.dev",
                "email":"inbox@ermiyas.dev",
                "about":"A software engineer that develop many system."
            }
            context_info = ""
            if context and context.get('recent_messages'):
                context_info += "\n\nPrevious conversation context:\n"
                for msg in context['recent_messages'][-4:]:  # Last 4 messages
                    context_info += f"{msg['role']}: {msg['content'][:200]}...\n"
            
            if context and context.get('corrections'):
                context_info += "\n\nUser corrections from previous interactions:\n"
                for correction in context['corrections']:
                    context_info += f"- {correction['correction'][:150]}...\n"
            
            if context and context.get('previous_analyses'):
                context_info += "\n\nPrevious analysis patterns:\n"
                for analysis in context['previous_analyses'][-2:]:  # Last 2 analyses
                    context_info += f"- Query: {analysis['query'][:100]}... (Type: {analysis['result_type']})\n"
            
            prompt = f"""
            You are an expert Data Analyst with memory of previous conversations.
            You have access to a pandas dataframe variable named `df`.
            The dataframe has these columns: {df}
            
            {context_info}
            
            Current User Question: "{user_query}"
            
            Instructions:
1. Consider the conversation history and any corrections the user has made
2. Write Python code using pandas to answer the question
3. If the user corrected you before, avoid making the same mistakes
4. Assign the final result to a variable named `result`
5. Output ONLY the python code without any explanations
6. Use only these libraries: pandas, matplotlib, seaborn, plotly
7. If you need to create a visualization, use plotly and assign to `fig`
8. Format: ```python\n# your code here\n```

Important: Only output the code, no other text. Learn from previous corrections.

            """ 
            result = ais.safe_completion(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            
            generated_code = result.choices[0].message.content
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()
            # print("generated code,", generated_code)
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
  
    def format_executed_code(self, result, error,user_query = None, df = None):
        print('format code,', result, error)
        if error:
            return {
                "type": "error",
                "content": error,
                "display": f"Error: {error}",
                "visualization": None,
                "narrative": None
            } 
        visualization = AutoVisualization()
        naration  = NarationSummary()
        visualization = visualization.create_visualization(result)
        print('visualizations,', visualization)

        narate = None
        if user_query and df is not None and error is None and result is not None:
            narate = naration.generate_summary(user_query,result,df)
        if result is None:
            return {
                "type": "empty",
                "content": None,
                "display": "No result returned from the analysis.",
                "visualization": None,
                "narrative": None
            }
        elif isinstance(result, pd.DataFrame):
            return {
                "type": "dataframe",
                "content": result,
                "display": "Analysis Result (DataFrame): ",
                "visualization": visualization,
                "narrative": narate
            }
        elif isinstance(result, (int, float)):
            return {
                "type": "number",
                "content": result,
                "display": f"Result: ",
                "visualization": None,
                "narrative": narate
            }
        elif isinstance(result, str):
            return {
                "type": "text",
                "content": result,
                "display": f"Result:",
                "visualization": None,
                "narrative": narate
            }
        else:
            return {
                "type": "unknown",
                "content": str(result),
                "display": f"Result:",
                "visualization": visualization,
                "narrative": narate
            }    