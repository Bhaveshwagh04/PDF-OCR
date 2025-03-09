import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title("📊 Dynamic Chart Generator")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Function to determine chart type
def determine_chart_type(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    if len(df.columns) == 2:
        if len(num_cols) == 1 and len(df) > 10:
            return 'histogram'
        elif len(num_cols) == 1 and len(df) <= 10:
            return 'pie'
        elif len(num_cols) == 2:
            return 'scatter'
        elif len(num_cols) == 1 and len(cat_cols) == 1:
            return 'bar'
    elif len(num_cols) >= 2:
        if len(num_cols) > 2:
            return 'heatmap'
        else:
            return 'line'
    elif len(cat_cols) > 0 and len(num_cols) > 0:
        return 'box'
    return None

# Function to generate the appropriate chart
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

    elif chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1],
                         title=f"Scatter Plot of {df.columns[0]} vs. {df.columns[1]}",
                         template="plotly_white")

    elif chart_type == 'histogram':
        fig = px.histogram(df, x=df.columns[0],
                           title=f"Distribution of {df.columns[0]}",
                           template="plotly_white")

    elif chart_type == 'box':
        fig = px.box(df, x=df.columns[0], y=df.columns[1],
                     title=f"Box Plot of {df.columns[0]} vs. {df.columns[1]}",
                     template="plotly_white")

    elif chart_type == 'heatmap':
        corr_matrix = df.select_dtypes(include=[np.number]).corr()
        fig = px.imshow(corr_matrix, 
                        x=corr_matrix.columns,
                        y=corr_matrix.index,
                        color_continuous_scale='Viridis',
                        title="Heatmap of Numerical Features")

    else:
        st.write("No suitable chart type determined for this data.")
        return
    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# Load and display data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### 📋 Preview of Uploaded Data", df.head())

    chart_type = determine_chart_type(df)
    
    if chart_type:
        st.write(f"### 📈 Recommended Chart Type: **{chart_type.capitalize()}**")
        generate_chart(df, chart_type)
    else:
        st.write("⚠️ No suitable chart type found for the dataset.")

