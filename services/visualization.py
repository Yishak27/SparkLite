import pandas as pd
import plotly.express as px

class AutoVisualization:
    def __init__(self):
        self.supported_charts = ['bar', 'line', 'pie']
    def should_visualize(self, result):
        if result is None:
            return False
        if isinstance(result, pd.DataFrame):
            if len(result) == 0:
                return False
            # Check if DataFrame has numeric columns and suitable structure
            numeric_cols = result.select_dtypes(include=['number']).columns
            if len(numeric_cols) == 0:
                return False
                
            # Check if it has categorical/text columns for grouping
            cat_cols = result.select_dtypes(include=['object', 'category']).columns
            date_cols = result.select_dtypes(include=['datetime64']).columns
            
            return len(result) > 1 and (len(cat_cols) > 0 or len(date_cols) > 0 or len(numeric_cols) > 1)
        elif isinstance(result, pd.Series):
            return len(result) > 1 and (result.dtype in ['number', 'object', 'category'] or 
                                      'datetime' in str(result.dtype))
        
        return False
                       
    def detect_chart_type(self,result):
        if not self.should_visualize(result):
            return None
        if isinstance(result, pd.DataFrame):
            numeric_cols = result.select_dtypes(include=['number']).columns
            cat_cols = result.select_dtypes(include=['object', 'category']).columns
            date_cols = result.select_dtypes(include=['datetime64']).columns
            
            # Time series detection
            if len(date_cols) > 0 and len(numeric_cols) > 0:
                return 'line'
            elif len(cat_cols) > 0 and len(numeric_cols) > 0:
                if len(result) <= 10: 
                    return 'pie'
                else: 
                    return 'bar'
            elif len(numeric_cols) == 1 and len(cat_cols) == 0:
                return 'bar'
            elif isinstance(result, pd.Series):
                if 'datetime' in str(result.dtype):
                    return 'line'
                elif result.dtype in ['object', 'category']:
                    return 'bar' if len(result.value_counts()) > 6 else 'pie'
                elif result.dtype in ['number']:
                    return 'bar'
        
        return 'bar'
        
    def create_visualization(self, result, chart_type=None):
        if not self.should_visualize(result):
            return None
        
        if chart_type is None:
            chart_type = self.detect_chart_type(result)

        if chart_type not in self.supported_charts:
            chart_type = 'bar'

        try:
            if chart_type == 'bar':
                return self._create_bar_chart(result)
            elif chart_type == 'line':
                return self._create_line_chart(result)
            elif chart_type == 'pie':
                return self._create_pie_chart(result)
        except Exception as e:
            print("visualization creation error, ", e)
            return None 


    def _create_bar_chart(self, result):

        if isinstance(result, pd.DataFrame):
            numeric_cols = result.select_dtypes(include=['number']).columns
            cat_cols = result.select_dtypes(include=['object', 'category']).columns
            
            if len(cat_cols) > 0 and len(numeric_cols) > 0:
                x_col = cat_cols[0]
                y_col = numeric_cols[0]
                fig = px.bar(result, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            else:
                fig = px.bar(result, title="Data Analysis")
        
        elif isinstance(result, pd.Series):
            if result.dtype in ['object', 'category']:
                value_counts = result.value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values, 
                           title=f"Distribution of {result.name}")
            else:
                fig = px.bar(y=result.values, title=f"Values of {result.name}")
        return fig


    def _create_line_chart(self, result):
        return " again line chart"
    def _create_pie_chart(self, result):
        return "pie chart"
    