import streamlit as st
import pandas as pd
 
st.title("SparkLite AI")
st.header("This is a simple AI agent that do sales analysis.")
st.write("Welcome to SparkLite AI")
 
df = pd.read_csv("sales_data.csv")
st.line_chart(df, x="product", y="total_price")