import streamlit as st
from kbcstorage.client import Client

def connection_details():
    """
    This function is used to enter the connection details for Keboola Storage.
    """

    st.session_state['connection_url'] = st.sidebar.selectbox('Connection URL', 
                                                    ['https://connection.keboola.com/', 
                                                    'https://connection.north-europe.azure.keboola.com/', 
                                                    'https://connection.eu-central-1.keboola.com/'])
    
    st.session_state['api_token'] = st.sidebar.text_input('API Token', 'Enter Password', type="password")
    
    if st.sidebar.button('Connect', key='connect'):
            if ('client') not in st.session_state:
                try:
                    st.session_state['client'] = Client(st.session_state['connection_url'],  st.session_state['api_token'])
                except Exception as e:
                    st.error('Please check your connection details')
                    st.error(e)
                  
            else:
                try:
                    if ('client') in st.session_state:
                        st.session_state['client'] = Client(st.session_state['connection_url'],  st.session_state['api_token']) 
                        st.session_state['client'].buckets.list()
                        st.sidebar.success('Connected to Keboola Storage')
                except Exception as e:
                    st.sidebar.error('Could not connect to Keboola Storage')
                    st.error(e)
                    

            return st.session_state['connection_url'], st.session_state['api_token'], st.session_state['client']

if __name__ == '__main__':
    connection_details()