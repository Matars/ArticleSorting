import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Function to connect to the database and retrieve data
def get_data_for_visualization():
    conn = sqlite3.connect('Faktajouren.db')
    query = """
        SELECT Begrepp, COUNT(*) as Frequency
        FROM faktajouren
        GROUP BY Begrepp
        ORDER BY Frequency DESC
        LIMIT 20
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Initialize Streamlit app
st.set_page_config(layout="wide")
st.title('Article Keyword Visualization')

# Retrieve data
df = get_data_for_visualization()

# Generate Plotly visualization
fig = px.bar(df, x='Frequency', y='Begrepp', orientation='h',
             title='Top 20 Keywords by Frequency')
fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=700)

# Display Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
