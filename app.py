import streamlit as st
from src.keboola_storage_api.connection import add_keboola_table_selection
#from src.keboola_storage_api.upload import main as upload_to_keboola
from src.st_aggrid import st_aggrid
from src.workspace_connection import workspace_connection as ws_connection
from src.fb_prophet_forecasting import st_prophet_forecast
import pandas as pd
#from src.codex_query_generator import codex

st.image('static/keboola_logo.png', width=400)

# Web App Title
st.markdown('''
# **Keboola Cookiecutter Streamlit App**

### This is a cookiecutter template for developing streamlit apps on top of the Keboola Storage API. 
---
''')

#ws_connection.connect_to_snowflake()

# Adds a table selection form to the sidebar of streamlit
add_keboola_table_selection()

if "uploaded_file" in st.session_state:
    query_df = pd.read_csv(st.session_state['uploaded_file'])
    #uncomment the following lines to enable the interactive table app

    st.subheader('Interactive Table')
    st.write(
    "This is a simple table app that uses the Keboola Storage API to get the data from the selected table."
    )
    st_aggrid.interactive_table()

    st.markdown('''
    ---
    ''')
    st.subheader('Prophet Forecasting')
    st.markdown('''
    This app allows you to generate forecasts using the Prophet library.
    ---
    ''')
    st_prophet_forecast.forecast(query_df)

    #upload_to_keboola()