import streamlit as st
from src.keboola_storage_api import connection_details as kbc_connection_details
from src.keboola_storage_api import table_selection as kbc_table_selection
from src.keboola_storage_api import table_selection_simple as kbc_table_selection_simple
from src.st_aggrid import st_aggrid
<<<<<<< HEAD
from src.workspace_connection import workspace_connection as ws_connection
from src.fb_prophet_forecasting import st_prophet_forecast
import pandas as pd
from src.codex_query_generator import codex
=======
from src.fb_prophet_forecasting import st_prophet_forecast
#from src.codex_query_generator import codex
>>>>>>> b6efcdf76e45223210b663a919d6821a0e4f2a89

st.image('static/keboola_logo.png', width=400)

# Web App Title
st.markdown('''
# **Keboola Cookiecutter Streamlit App**

### This is a cookiecutter template for developing streamlit apps on top of the Keboola Storage API. 
---
''')

#ws_connection.connect_to_snowflake()

kbc_connection_details.connection_details()

kbc_table_selection_simple.table_selection()

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


if st.button('Generate Queries'):
    st.subheader('Generate Queries')
    codex.codex()
