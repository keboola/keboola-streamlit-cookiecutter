import streamlit as st
import pandas as pd
from kbcstorage.client import Client

def table_selection():
    with st.sidebar.header('Select a bucket from storage'):
        try:
            client = Client(st.session_state['connection_url'],  st.session_state['api_token'])
        except Exception as e:
            st.error('Please check your connection details')
            st.error(e)

        def callback():
            st.sidebar.success('Connected to Keboola Storage')
        
        
        def get_buckets():
            """ 
            This function is used to get the list of buckets from Keboola Storage.
            """
            try:
                bucket_names = []
                for i in client.buckets.list():
                    bucket_names.append(i['name'])

            except Exception as e:
                st.error('Could not list buckets')
                st.error(e)
                # Select a bucket from the list

          
            bucket = st.sidebar.selectbox('Bucket', bucket_names, on_change=callback)
           

            # get the id of the selected bucket
            
            for i in client.buckets.list():
                if i['name'] == bucket:
                    bucket_id = i['id']
                
            return bucket_id

    bucket_id = get_buckets()

    # Get the list of tables from the selected bucket
    with st.sidebar.header('Select a table from the bucket'):
                        # Select a table from the bucket
        @st.experimental_memo(suppress_st_warning=True)
        def get_tables(bucket_id):
            """
            This function is used to get the list of tables from the selected bucket.
            """
            table_names = []
            try:
                for i in st.session_state['client'].buckets.list_tables(bucket_id):
                    table_names.append(i['name'])
            except Exception as e:
                st.error('Could not list tables')
                st.error(e)
        
            # Select a table from the list
            table = st.sidebar.selectbox('table', table_names, on_change=callback)

            # get the id of the selected table
            for i in st.session_state['client'].tables.list(bucket_id):
                if i['name'] == table:
                    table_id = i['id']
            return table_id     
        
        try:
            table_id = get_tables(bucket_id)
            st.session_state['uploaded_file'] = st.session_state['client'].tables.export_to_file(table_id=table_id, path_name='.')
        except Exception as e:
            st.error('Could not get the table')
            st.error(e)
        
        if ['uploaded_file'] in st.session_state:
            st.write('File uploaded successfully')
            return st.session_state['uploaded_file']

if __name__ == '__main__':
    table_selection()