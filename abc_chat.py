import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd

def determine_chart_type(df):
    if len(df.columns) == 2:
        if np.issubdtype(df.dtypes[1], np.number) and len(df) > 1:
            return 'bar'
        elif np.issubdtype(df.dtypes[1], np.number) and len(df) <= 10:
            return 'pie'
    elif len(df.columns) >= 3 and np.issubdtype(df.dtypes[1], np.number):
        return 'line'
    return None

def generate_chart(df, chart_type):
    if chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                     title=f"{df.columns[0]} vs. {df.columns[1]}",
                     template="plotly_white")
    elif chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                     title=f"Distribution of {df.columns[0]}",
                     template="plotly_white")
    elif chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1],
                      title=f"{df.columns[1]} Over {df.columns[0]}",
                      template="plotly_white", markers=True)
    else:
        st.write("No suitable chart type determined for this data.")
        return
    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

#Example usage:
df = pd.DataFrame({'Category': ['A', 'B', 'C'], 'Value': [10, 20, 30]})
chart_type = determine_chart_type(df)
if chart_type:
    generate_chart(df, chart_type)
else:
     st.write("No suitable chart type determined for this data.")
