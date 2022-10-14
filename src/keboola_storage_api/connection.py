import streamlit as st
import os
from requests.exceptions import HTTPError
from typing import Dict, List, Tuple

from kbcstorage.client import Client

KBC_URLS = ['https://connection.keboola.com/',
            'https://connection.north-europe.azure.keboola.com/',
            'https://connection.eu-central-1.keboola.com/']


def add_keboola_table_selection():
    """
        This function is used to initialize all forms to deal with loading a table from Keboola Storage.
        - The Connection Form enters the KBC URL and API Token
        - The Bucket Form enters the selected bucket
        - The Table Form enters the selected table

        The Bucket Form only appears once a connection is made
        The Table Form only appears when a Bucket is selected

    """
    _add_connection_form()
    if "kbc_storage_client" in st.session_state:
        _add_bucket_form()
    if "selected_bucket" in st.session_state and "kbc_storage_client" in st.session_state:
        _add_table_form()


def _add_connection_form():
    with st.sidebar.form("Connection Details"): 
        connection_url = st.selectbox('Connection URL', KBC_URLS)
        api_key = st.text_input('API Token', 'Enter Password', type="password")
        if st.form_submit_button("Connect"):

            # Reset Client
            if "kbc_storage_client" in st.session_state:
                st.session_state.pop("kbc_storage_client")

            # Clear selected buckets and tables if connection is reset
            if "selected_table" in st.session_state:
                st.session_state.pop("selected_table")
            if "selected_table_id" in st.session_state:
                st.session_state.pop("selected_table_id")
            if "selected_bucket" in st.session_state:
                st.session_state.pop("selected_bucket")
            if "uploaded_file" in st.session_state:
                st.session_state.pop("uploaded_file")

            kbc_client = Client(connection_url, api_key)
            if _get_bucket_list(kbc_client):
                st.session_state['kbc_storage_client'] = kbc_client
                st.session_state['bucket_list'] = _get_bucket_list(kbc_client)


def _add_bucket_form():
    with st.sidebar.form("Bucket Details"):
        with st.header('Select a bucket from storage'):
            bucket = st.selectbox('Bucket', _get_buckets_from_bucket_list())
        if st.form_submit_button("Select Bucket"):
            st.session_state['selected_bucket'] = bucket


def _add_table_form():
    with st.sidebar.form("Table Details"):
        table_names, tables = _get_tables(st.session_state['selected_bucket'])
        st.session_state['selected_table'] = st.selectbox('Table', table_names)
        st.session_state['selected_table_id'] = tables[st.session_state['selected_table']]["id"]
        if st.form_submit_button("Select table"):
            st.session_state['kbc_storage_client'].tables.export_to_file(
                table_id=st.session_state['selected_table_id']
                )
            st.session_state['uploaded_file'] = os.path.join(st.session_state['selected_table'])


def _get_bucket_list(kbc_storage_client):
    try:
        project_bucket_list = kbc_storage_client.buckets.list()
        return project_bucket_list
    except HTTPError:
        st.error("Invalid Connection settings")


def _get_buckets_from_bucket_list():
    """
    This function is used to get the list of buckets from Keboola Storage.
    """
    try:
        return [bucket['id'] for bucket in st.session_state['bucket_list']]
    except Exception:
        st.error('Could not list buckets')


def _get_tables(bucket_id: str) -> Tuple[List, Dict]:
    try:
        tables = {}
        for table in st.session_state['kbc_storage_client'].buckets.list_tables(bucket_id):
            tables[table['name']] = table
        table_names = list(tables.keys())
        return table_names, tables
    except Exception as e:
        st.error('Could not list tables')
        st.error(e)