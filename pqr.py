import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

def determine_chart_type(df):
    """
    Determine the chart type based on the number of columns and data types.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    str: The chart type ('bar', 'pie', 'line', 'scatter', 'heatmap', or 'histogram').
    """
    if len(df.columns) == 1:
        if df.dtypes[0] in ['int64', 'float64']:
            return 'histogram'
    elif len(df.columns) == 2:
        if df.dtypes[0] in ['int64', 'float64'] and df.dtypes[1] in ['int64', 'float64']:
            return 'scatter'
        elif df.dtypes[1] in ['int64', 'float64'] and len(df) > 1:
            return 'bar'
        elif df.dtypes[1] in ['int64', 'float64'] and len(df) <= 10:
            return 'pie'
    elif len(df.columns) >= 3:
        if df.dtypes[0] in ['object', 'category'] and df.dtypes[1] in ['object', 'category'] and df.dtypes[2] in ['int64', 'float64']:
            return 'heatmap'
        elif df.dtypes[1] in ['int64', 'float64']:
            return 'line'
    return None

def generate_chart(df, chart_type, title=None, x_axis_label=None, y_axis_label=None, color_scale=None, bin_size=None):
    """
    Generate a chart based on the chart type.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    chart_type (str): The chart type ('bar', 'pie', 'line', 'scatter', 'heatmap', or 'histogram').
    title (str): The chart title.
    x_axis_label (str): The x-axis label.
    y_axis_label (str): The y-axis label.
    color_scale (str): The color scale for heatmaps.
    bin_size (int): The bin size for histograms.
    """
    if chart_type is None:
        st.write("No suitable chart type determined for this data.")
        return
    
    if df.empty:
        st.write("The input DataFrame is empty.")
        return
    
    if chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                     title=title if title else f"{df.columns[0]} vs. {df.columns[1]}",
                     template="plotly_white", color=df.columns[0])
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                     title=title if title else f"Distribution of {df.columns[0]}",
                     template="plotly_white")
    elif chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1],
                      title=title if title else f"{df.columns[1]} Over {df.columns[0]}",
                      template="plotly_white", markers=True)
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1],
                         title=title if title else f"{df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'heatmap':
        fig = px.imshow(df.pivot_table(index=df.columns[0], columns=df.columns[1], values=df.columns[2]),
                         text_auto=True,
                         title=title if title else f"Heatmap of {df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white",
                         color_continuous_scale=color_scale if color_scale else "Viridis")
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=df.columns[0],
                           title=title if title else f"Histogram of {df.columns[0]}",
                           template="plotly_white",
                           nbins=bin_size if bin_size else 10)
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# Example usage:
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': [10, 20, 30, 40, 50]
})
chart_type = determine_chart_type(df)
generate_chart(df, chart_type, title="Example Chart", x_axis_label="Category", y_axis_label="Value")

df2 = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [2, 4, 6, 8, 10]
})
chart_type2 = determine_chart_type(df2)
generate_chart(df2, chart_type2, title="Scatter Plot Example", x_axis_label="X", y_axis_label="Y")

df3 = pd.DataFrame({
    'Category1': ['A', 'B', 'C', 'D', 'E'],
    'Category2': ['X', 'Y', 'Z', 'W', 'V'],
    'Value': [10, 20, 30, 40, 50]
})
chart_type3 = determine_chart_type(df3)
generate_chart(df3, chart_type3, title="Heatmap Example", color_scale="Plasma")

df4 = pd.DataFrame({
    'Value': [10, 20, 30, 40, 50]
})
chart_type4 = determine_chart_type(df4)
generate_chart(df4, chart_type4, title="Histogram Example", bin_size=5)