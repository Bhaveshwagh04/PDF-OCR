import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def determine_chart_type(df):
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    # Check for Pie Chart: 1 categorical + 1 numerical, limited categories (&lt;=10)
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

    # Check for Gauge Chart: 1 categorical + 1 numerical, with few rows (&lt;=5)
    if len(df.columns) == 2 and len(num_cols) == 1 and len(cat_cols) == 1 and len(df) <= 5:
        return 'gauge'

    # Default case
    return None

def generate_chart(df, chart_type, title, x_axis_label, y_axis_label):
    if chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=df.columns[0], title=title)
        fig.update_layout(xaxis_title=x_axis_label)
    elif chart_type == 'heatmap':
        fig = px.imshow(df, text_auto=True, title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'bubble':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], size=df.columns[2], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'radar':
        fig = px.line_polar(df, r=df.columns[1], theta=df.columns[0], title=title)
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, df[df.columns[1]].max() * 1.1])))
    elif chart_type == 'area':
        fig = px.area(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'dot':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=title)
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'treemap':
        fig = px.treemap(df, names=df.columns[0], parents=[''] * len(df), values=df.columns[1], title=title)
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    elif chart_type == 'gauge':
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = df[df.columns[1]].mean(),
            title = {'text': title},
            delta = {'reference': df[df.columns[1]].mean() * 0.5, 'increasing': {'color': "RebeccaPurple"}},
            threshold = {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': df[df.columns[1]].mean() * 0.75},
        ))
        fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    elif chart_type == 'waterfall':
        fig = go.Figure(go.Waterfall(
            x=df.columns[0],
            y=df.columns[1],
            name=title
        ))
        fig.update_layout(title=title, xaxis_title=x_axis_label, yaxis_title=y_axis_label)
    else:
        fig = None

    if fig:
        fig.show()

# Example usage:
df10 = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': [10, 20, 30, 40, 50]
})

chart_type = determine_chart_type(df10)
if chart_type:
    generate_chart(df10, chart_type, title="Chart Example", x_axis_label="Category", y_axis_label="Value")
else:
    generate_chart(df10, 'waterfall', title="Waterfall Example", x_axis_label="Category", y_axis_label="Value")