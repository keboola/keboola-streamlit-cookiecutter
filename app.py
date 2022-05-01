import streamlit as st
from src.keboola_storage_api import connection_details as kbc_connection_details
from src.keboola_storage_api import table_selection as kbc_table_selection

# Web App Title
st.markdown('''
# **Keboola Cookiecutter Streamlit App**

This is a cookiecutter template for developing streamlit apps ontop of the Keboola Storage API. 
---
''')

kbc_connection_details.connection_details()

kbc_table_selection.table_selection()