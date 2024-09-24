# This is a sample Python script.
#How to cite: Statistics Canada. Table 18-10-0006-01  Consumer Price Index, monthly, seasonally adjusted
#DOI: https://doi.org/10.25318/1810000601-eng
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import streamlit.components.v1 as components


# Sample data (replace with your actual DataFrame)
data = pd.read_csv('cpi_canada_cleaned.csv')

df = pd.DataFrame(data)

df['Date'] = pd.to_datetime(df['Date'])

# Define a mapping for renaming columns
rename_mapping = {
    'alcoholic_beverages__tobacco_products_and_recreational_cannabis': 'Alcohol, Tobacco, Cannabis',
    'allitems_8': 'All Items',
    'clothing_and_footwear': 'Clothing & Footwear',
    'food': 'Food',
    'health_and_personal_care': 'Health & Personal Care',
    'household_operations__furnishings_and_equipment': 'Household Operations',
    'recreation__education_and_reading': 'Recreation & Education',
    'shelter': 'Shelter',
    'transportation': 'Transportation'
}

# Rename the columns in the DataFrame
df.rename(columns=rename_mapping, inplace=True)


items = ['All Items', 'Food', 'Clothing & Footwear', 'Health & Personal Care',
         'Household Operations','Recreation & Education', 'Shelter', 'Transportation', 'Alcohol, Tobacco, Cannabis']

# Initialize Streamlit app
st.title("Canada CPI Analysis and Prediction")

# Create a button to start the animation
start_button = st.button("Start Animation")

if start_button:
    # Initialize a Plotly figure
    fig = go.Figure()

    # Add initial bar chart (start at 0 for all bars)
    fig.add_trace(go.Bar(
        y=items,
        x=[0] * len(items),  # Starting with zero values
        orientation='h',
        marker=dict(color=['#7FD5EE', '#FFA500', '#003342', '#FF7F50', '#6A5ACD', '#32CD32', '#FF69B4', '#FFD700', '#FF4500']),
        name="Values"
    ))

    # Set up layout (initial)
    fig.update_layout(
        xaxis=dict(range=[0, df[items].max().max() + 5], title="Values"),
        yaxis=dict(title="Items"),
        title="Progression of Canada CPI Values Over Time (1992-01 to 2024-08) ",
        showlegend=False,
    )

    # Display the initial plot in Streamlit
    bar_chart = st.plotly_chart(fig)

    # Animation loop
    for i in range(len(df)):
        # Update the bar chart values for the next step
        fig.data[0].x = [df[item][i] for item in items]  # Update bars with next row's values

        # Update the date annotation
        fig.update_layout(
            annotations=[
                dict(
                    x=0.95,
                    y=0.05,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    text=f"Date: {df['Date'][i].strftime('%Y-%m')}",
                    font=dict(size=14, color="black"),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            ]
        )

        # Redraw the updated figure
        bar_chart.plotly_chart(fig)

        # Add a short delay to simulate animation effect
        time.sleep(0.01)

# 2. Line Plot for Items Over Time
st.subheader("Line Plot of CPI Values Over Time")

# Plot the line chart using Plotly Express
line_fig = px.line(df, x='Date', y=items,
                   labels={'value': 'Value', 'variable': 'Item'},
                   title="CPI Values Over Time",
                   template="plotly_dark")

# Display the line plot
st.plotly_chart(line_fig)


# Function to display the HTML file containing the Plotly figure
def display_html(file_path):
    with open(file_path, 'r') as f:
        html_string = f.read()
    components.html(html_string, height=600)  # Adjust the height as needed

# Title of the Streamlit app
st.title("Combined Predicted CPI Prices For next 8 months (2024-09 to 2025-04")

# Display the combined Plotly graph
display_html('combined_plot.html')

# Title for the section
st.title("Projected Percentage Change Over the Next 8 Months")

# Display the inference and conclusion
st.subheader("Inference and Conclusion")

# Shelter
st.write("### Shelter (3.58% Increase):")
st.write("""
The most significant projected increase is seen in the shelter category, suggesting continued upward pressure on housing costs. This could be driven by factors such as increasing demand for housing, limited supply, or rising mortgage rates. It's critical to monitor the housing market as it will significantly impact household budgets.
""")

# Transportation
st.write("### Transportation (2.67% Increase):")
st.write("""
Transportation is also expected to experience a substantial increase. Rising fuel costs or fluctuations in the automotive market (e.g., vehicle prices, maintenance costs) might contribute to this change. Given the impact of transportation on everyday life, this could lead to higher overall living costs.
""")

# Health & Personal Care
st.write("### Health & Personal Care (2.3% Increase):")
st.write("""
This category's projected growth suggests increasing healthcare costs or higher prices for personal care items. Inflation in this area could be due to rising medical service fees or more expensive personal care products.
""")

# Food
st.write("### Food (1.92% Increase):")
st.write("""
The food category shows a significant rise, indicating potential inflationary pressure in the cost of groceries. This could stem from supply chain disruptions, increased production costs, or shifts in global food markets. Rising food prices may contribute to overall inflation.
""")

# Recreation & Education
st.write("### Recreation & Education (1.4% Increase):")
st.write("""
The rise in recreation and education costs points to increased prices in leisure activities and educational services. This might reflect higher costs for entertainment, cultural events, or educational materials.
""")

# All Items
st.write("### All Items (1.46% Increase):")
st.write("""
The overall CPI forecast shows a modest increase of 1.46%, suggesting a general inflationary trend over the next 8 months. This indicates a consistent rise in the cost of living across multiple sectors.
""")

# Alcohol, Tobacco, and Cannabis
st.write("### Alcohol, Tobacco, and Cannabis (0.74% Increase):")
st.write("""
The relatively smaller increase in alcohol, tobacco, and cannabis suggests moderate price stability in these areas. Government regulations, taxation, and controlled markets may help keep price volatility in check.
""")

# Clothing & Footwear and Household Operations
st.write("### Clothing & Footwear (0.35% Increase) and Household Operations (0.36% Increase):")
st.write("""
These categories exhibit the lowest projected inflation rates, indicating relatively stable prices for apparel and household services. This may reflect less immediate pressure from supply chain issues or consumer demand in these sectors.
""")