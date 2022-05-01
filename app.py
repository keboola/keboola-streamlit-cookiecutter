import streamlit as st
from src.keboola_storage_api import connection_details as kbc_connection_details
from src.keboola_storage_api import table_selection as kbc_table_selection
from src.st_aggrid import st_aggrid

# Web App Title
st.markdown('''
# **Keboola Cookiecutter Streamlit App**

This is a cookiecutter template for developing streamlit apps on top of the Keboola Storage API. 
---
''')

kbc_connection_details.connection_details()

kbc_table_selection.table_selection()

st.markdown('''
Choose which apps you want to run.
---
''')

if st.button('Interactive Table'):
    st.subheader('Interactive Table')
    st.markdown('''
    This app shows a table with the selected table.
    ---
    ''')
    st_aggrid.interactive_table()
    