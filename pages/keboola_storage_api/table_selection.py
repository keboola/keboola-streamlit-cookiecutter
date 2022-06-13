import streamlit as st
import pandas as pd
from kbcstorage.client import Client

def table_selection():
    with st.sidebar.header('Select a bucket from storage'):
        if ('client') not in st.session_state:
                try:
                    st.session_state['client'] = Client(st.session_state['connection_url'],  st.session_state['api_token'])
                except Exception as e:
                    st.error('Please check your connection details')
                    st.error(e)

        def callback():
            st.sidebar.success('Connected to Keboola Storage')
        
        
        def get_buckets():
            """ 
            This function is used to get the list of buckets from Keboola Storage.
            """
            #if ('bucket') in st.session_state:
            #    st.session_state.pop('bucket')
            #if ('table_names') in st.session_state:
            #    st.session_state.pop('table_names')
            if ('bucket_names') not in st.session_state:
                try:
                    st.session_state.bucket_names = []

                    for i in st.session_state['client'].buckets.list():
                        st.session_state.bucket_names.append(i['name'])

                except Exception as e:
                    st.error('Could not list buckets')
                    st.error(e)
                # Select a bucket from the list
            if st.session_state['bucket_names'] in st.session_state:
                st.session_state['bucket'] = st.sidebar.selectbox('Bucket', st.session_state.bucket_names)
            else: 
                st.write('no bucket selected')

            # get the id of the selected bucket
     

            #if ('bucket_id') in st.session_state:
            #   return st.session_state['bucket_id']
    
        st.session_state['bucket_id'] = get_buckets()
        for i in st.session_state['client'].buckets.list():
            if i['name'] == st.session_state['bucket']:
                st.session_state['bucket_id'] = i['id']
                
    

    # Get the list of tables from the selected bucket
    with st.sidebar.header('Select a table from the bucket'):
                        # Select a table from the bucket
        def get_tables():
            """
            This function is used to get the list of tables from the selected bucket.
            """
            if ('bucket_id') in st.session_state:
                st.session_state.table_names = []
                try:
                    for i in st.session_state['client'].buckets.list_tables(st.session_state['bucket_id']):
                        st.session_state.table_names.append(i['name'])
                except Exception as e:
                    st.error('Could not list tables')
                    st.error(e)
            
            # Select a table from the list
            st.session_state['table'] = st.sidebar.selectbox('Table', st.session_state.table_names)

            # get the id of the selected table
            for i in st.session_state['client'].tables.list(st.session_state['bucket_id']):
                if i['name'] == st.session_state['table']:
                    st.session_state['table_id'] = i['id']
                    break
                    
        return st.session_state['table_id']
        

        
        
        try:
            st.session_state['table_id'] = get_tables()
            st.session_state['uploaded_file'] = st.session_state['client'].tables.export_to_file(table_id=st.session_state['table_id'], path_name='.')
        except Exception as e:
            st.error('Could not get the table')
            st.error(e)
        
        if ['uploaded_file'] in st.session_state:
            st.write('File uploaded successfully')
            return st.session_state['uploaded_file']

if __name__ == '__main__':
    table_selection()