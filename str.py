import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

def determine_chart_type(df):
    """
    Determine the most suitable chart type based on the structure of the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing data to be visualized.

    Returns:
    str: The suggested chart type. Returns None if no suitable chart type is found.

    Raises:
    ValueError: If the input is not a pandas DataFrame or if the DataFrame is empty.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    # Check for Pie Chart: 1 categorical + 1 numerical, limited categories (<=10)
    if len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1 and len(df) <= 10:
        return 'pie'

    # Check for Line Chart: Time-based or sequential data with at least one numerical column
    if len(df.columns) >= 2 and len(num_cols) > 0:
        time_columns = [col.lower() for col in df.columns]
        if any(word in time_columns for word in ['month', 'year', 'date', 'time', 'day']):
            return 'line'

    # Check for Scatter Plot: At least 2 numerical columns
    if len(num_cols) >= 2:
        return 'scatter'

    # Check for Histogram: Only 1 numerical column
    if len(df.columns) == 1 and len(num_cols) == 1:
        return 'histogram'

    # Check for Heatmap: Only numerical data with multiple columns
    if len(df.columns) > 1 and len(num_cols) == len(df.columns):
        return 'heatmap'

    # Check for Bubble Chart: At least 3 numerical columns
    if len(num_cols) >= 3:
        return 'bubble'

    # Check for Radar Chart: 1 categorical + multiple numerical columns
    if len(df.columns) > 2 and len(num_cols) > 1 and len(cat_cols) == 1:
        return 'radar'

    # Check for Bar Chart: 1 categorical + 1 numerical, or multiple categorical columns
    if (len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1) or \
       (len(df.columns) > 2 and len(cat_cols) > 0 and len(num_cols) > 0):
        return 'bar'

    # Check for Area Chart: 1 categorical + 1 numerical, or multiple numerical columns
    if (len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1) or \
       (len(df.columns) > 2 and len(num_cols) > 0):
        return 'area'

    # Check for Dot Plot: 1 categorical + 1 numerical
    if len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1:
        return 'dot'

    # Check for Treemap: 1 categorical + 1 numerical
    if len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1:
        return 'treemap'

    # Check for Gauge Chart: 1 categorical + 1 numerical, with few rows (<=5)
    if len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1 and len(df) <= 5:
        return 'gauge'

    # Default case
    return None

def generate_chart(df, chart_type, title=None, x_axis_label=None, y_axis_label=None, color_scale=None, bin_size=None):
    """
    Generate a chart based on the chart type.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    chart_type (str): The chart type ('bar', 'pie', 'line', 'scatter', 'heatmap', 'histogram', 'boxplot', 'violinplot', 'densityplot', 'treemap', 'sunburst', 'waterfall', 'funnel', 'sankey').
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
    elif chart_type == 'boxplot':
        fig = px.box(df, x=df.columns[0], y=df.columns[1],
                     title=title if title else f"Boxplot of {df.columns[0]} vs. {df.columns[1]}",
                     template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'violinplot':
        fig = px.violin(df, x=df.columns[0], y=df.columns[1],
                        title=title if title else f"Violinplot of {df.columns[0]} vs. {df.columns[1]}",
                        template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'densityplot':
        fig = px.density_heatmap(df, x=df.columns[0], y=df.columns[1],
                                 title=title if title else f"Densityplot of {df.columns[0]} vs. {df.columns[1]}",
                                 template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'treemap':
        fig = px.treemap(df, names=df.columns[0], parents=df.columns[1], values=df.columns[2],
                         title=title if title else f"Treemap of {df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white")
    elif chart_type == 'sunburst':
        fig = px.sunburst(df, names=df.columns[0], parents=df.columns[1], values=df.columns[2],
                          title=title if title else f"Sunburst of {df.columns[0]} vs. {df.columns[1]}",
                          template="plotly_white")
    elif chart_type == 'waterfall':
        fig = px.waterfall(df, x=df.columns[0], y=df.columns[1],
                            title=title if title else f"Waterfall of {df.columns[0]} vs. {df.columns[1]}",
                            template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'funnel':
        fig = px.funnel(df, x=df.columns[0], y=df.columns[1],
                         title=title if title else f"Funnel of {df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white")
        fig.update_xaxes(title=x_axis_label if x_axis_label else df.columns[0])
        fig.update_yaxes(title=y_axis_label if y_axis_label else df.columns[1])
    elif chart_type == 'sankey':
        fig = px.sankey(df, source=df.columns[0], target=df.columns[1], value=df.columns[2],
                         title=title if title else f"Sankey of {df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white")
    
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

df5 = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value1': [10, 20, 30, 40, 50],
    'Value2': [15, 25, 35, 45, 55]
})
chart_type5 = determine_chart_type(df5)
generate_chart(df5, 'boxplot', title="Boxplot Example", x_axis_label="Category", y_axis_label="Value")

df6 = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value1': [10, 20, 30, 40, 50],
    'Value2': [15, 25, 35, 45, 55]
})
chart_type6 = determine_chart_type(df6)
generate_chart(df6, 'violinplot', title="Violinplot Example", x_axis_label="Category", y_axis_label="Value")

df7 = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [2, 4, 6, 8, 10]
})
chart_type7 = determine_chart_type(df7)
generate_chart(df7, 'densityplot', title="Densityplot Example", x_axis_label="X", y_axis_label="Y")

df8 = pd.DataFrame({
    'Category1': ['A', 'B', 'C', 'D', 'E'],
    'Category2': ['X', 'Y', 'Z', 'W', 'V'],
    'Value': [10, 20, 30, 40, 50]
})
chart_type8 = determine_chart_type(df8)
generate_chart(df8, 'treemap', title="Treemap Example")

df9 = pd.DataFrame({
    'Category1': ['A', 'B', 'C', 'D', 'E'],
    'Category2': ['X', 'Y', 'Z', 'W', 'V'],
    'Value': [10, 20, 30, 40, 50]
})
chart_type9 = determine_chart_type(df9)
generate_chart(df9, 'sunburst', title="Sunburst Example")

df10 = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value1': [10, 20, 30, 40, 50],
    'Value2': [15, 25, 35, 45, 55]
})
chart_type10 = determine_chart_type(df10)
generate_chart(df10, 'waterfall', title="Waterfall Example", x_axis_label="Category", y_axis_label="Value")

df11 = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value1': [10, 20, 30, 40, 50],
    'Value2': [15, 25, 35, 45, 55]
})
chart_type11 = determine_chart_type(df11)
generate_chart(df11, 'funnel', title="Funnel Example", x_axis_label="Category", y_axis_label="Value")

df12 = pd.DataFrame({
    'Source': ['A', 'B', 'C', 'D', 'E'],
    'Target': ['X', 'Y', 'Z', 'W', 'V'],
    'Value': [10, 20, 30, 40, 50]
})
chart_type12 = determine_chart_type(df12)
generate_chart(df12, 'sankey', title="Sankey Example")