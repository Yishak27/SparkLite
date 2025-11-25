from openai import OpenAI
import pandas as pd
from .ai_generator import AICodeGenarator

class NarationSummary:
    def __init__(self):
        pass
    def generate_summary(self, user_query, result, df):
        ai = AICodeGenarator()
        try:
            if isinstance(result, pd.DataFrame):
                result_description = f"The result is a DataFrame with {len(result)} rows and {len(result.columns)} columns. First few values: {result.head(3).to_dict()}"

            elif isinstance(result, (int, float)):
                result_description = f"The result is a number: {result}"
            elif isinstance(result, pd.Series):
                result_description = f"The result is a Series: {result.head(10).to_dict()}"
            else:
                result_description = f"The result: {str(result)}"
            
            prompt = "Write exactly two sentences that explain what this data shows. Be specific and mention numbers or patterns."
            
            response = ai.safe_completion(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            # print('summary response, ', response)
            summary = response.choices[0].message.content.strip()
            print('summary,', summary)
            return summary
        except Exception as e:
            print('ai summary exception error:', e)
            return "Unable to generate summary."
        
