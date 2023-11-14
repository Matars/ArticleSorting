import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Function to connect to the database and run a query


def run_query(query, params):
    conn = sqlite3.connect('Faktajouren.db')
    result = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return result


# Streamlit app layout
st.set_page_config(layout="wide")  # Set the page to wide layout
st.title('Faktajouren Search and Filter Proof of Concept')

# Hide the "Made with Streamlit" footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header('Filters')
nummer_filter = st.sidebar.text_input('Filter by Nummer:', '')
begrepp_filter = st.sidebar.text_input('Filter by Begrepp:', '')
innehall_filter = st.sidebar.text_input('Filter by Innehåll:', '')
veckans_ord_filter = st.sidebar.text_input('Filter by Veckans ord:', '')
fria_sokord_termer_filter = st.sidebar.text_input(
    'Filter by Fria sökord / termer:', '')

# Build query
query = "SELECT * FROM faktajouren WHERE " + \
    "Nummer LIKE '%' || ? || '%' AND " + \
    "Innehall LIKE '%' || ? || '%' AND " + \
    "Begrepp LIKE '%' || ? || '%' AND " + \
    "Veckans_ord LIKE '%' || ? || '%' AND " + \
    "Fria_sokord_termer LIKE '%' || ? || '%'"

# Run query with filters
df = run_query(query, (nummer_filter, innehall_filter,
               begrepp_filter, veckans_ord_filter, fria_sokord_termer_filter))

# Display the results with better formatting
for _, row in df.iterrows():
    with st.expander(f"{row['Nummer']} - {row['Innehall']}"):
        st.write(f"Begrepp: {row['Begrepp']}")
        st.write(f"Veckans ord: {row['Veckans_ord']}")
        st.write(f"Faktcheck: {row['Faktcheck']}")
        # Making the link clickable
        st.markdown(f"Länk: [Link]({row['Lank']})")

