import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def run_query(query, params=None) -> pd.DataFrame:
    """Function to connect to the database and run a query

    Args:
        query (String): sql query
        params (tuple, optional): Search filters. Defaults to None.

    Returns:
        result: dataframe with the query result
    """
    conn = sqlite3.connect('Faktajouren.db')
    result = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return result


def get_unique_values(column_name) -> list:
    """Function to get unique values from a column with multiple entries

    Args:
        column_name (String): Database column to seach

    Returns:
        unique values: get unique (non repeating) database entries
    """
    query = f"SELECT {column_name} FROM faktajouren"
    result = run_query(query)
    all_values = result[column_name].tolist()

    unique_values = set()
    for value in all_values:
        # remove empty or new lines from value
        if value is not None and value != '':
            # Split the string by comma and strip white spaces
            entries = [entry.strip() for entry in value.split(',')]
            unique_values.update(entries)

    # remvoe all empty strings
    unique_values.discard('')
    return list(unique_values)


def display_tag_clouds(column_names) -> None:
    """Function to display tag clouds for each column, the tag clouds are generated from the unique values in the column

    Args:
        column_names (list): the columns to generate tag clouds for
    """
    num_columns = len(column_names)

    # Initialize a figure with enough width to accommodate all tag clouds
    plt.figure(figsize=(6 * num_columns, 3), dpi=200)

    for i, column_name in enumerate(column_names):
        # Fetch unique values and their counts
        all_values = df[column_name].str.split(',').explode().str.strip()
        values_count = all_values.value_counts().to_dict()

        # Generate the word cloud
        wordcloud = WordCloud(
            width=1200, height=600, background_color='#f9f1f1').generate_from_frequencies(values_count)

        # Add a subplot for the word cloud
        plt.subplot(1, num_columns, i + 1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(column_name)  # Add title to each subplot

    plt.tight_layout(pad=0.5)  # Increase padding between subplots

    # Convert to a format that can be displayed in Streamlit
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


# Streamlit app layout ----------------------------------------------
st.set_page_config(layout="wide")  # Set the page to wide layout
st.title('Faktajouren Search and Filter Proof of Concept')

# Hide the "Made with Streamlit" footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar filter fields
st.sidebar.header('Filters')
nummer_values = get_unique_values('Nummer')
nummer_filter = st.sidebar.selectbox('Filter by Nummer:', [''] + nummer_values)

begrepp_values = get_unique_values('Begrepp')
begrepp_filter = st.sidebar.selectbox(
    'Filter by Begrepp:', [''] + sorted(begrepp_values))

innehall_values = get_unique_values('Innehall')
innehall_filter = st.sidebar.selectbox(
    'Filter by Innehåll:', [''] + innehall_values)

veckans_ord_values = get_unique_values('Veckans_ord')
veckans_ord_filter = st.sidebar.selectbox(
    'Filter by Veckans ord:', [''] + veckans_ord_values)

fria_sokord_termer_values = get_unique_values('Fria_sokord_termer')
fria_sokord_termer_filter = st.sidebar.selectbox(
    'Filter by Fria sökord / termer:', [''] + fria_sokord_termer_values)

# Layour End ---------------------------------------------------------

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


with st.spinner(''):
    # TODO: sperate thread for loading cloud images, or cache the images
    display_tag_clouds(['Begrepp', 'Innehall', 'Veckans_ord'])

    # Display the results with better formatting
    for _, row in df.iterrows():
        with st.expander(f"{row['Nummer']} - {row['Innehall']}"):
            st.write(f"Begrepp: {row['Begrepp']}")
            st.write(f"Veckans ord: {row['Veckans_ord']}")
            st.write(f"Faktcheck: {row['Faktcheck']}")

            # Making the link clickable
            st.markdown(f"Länk: [Link]({row['Lank']})")
