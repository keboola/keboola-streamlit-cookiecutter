from io import StringIO
import os
import streamlit as st
from pathlib import Path
import keboola_api as kb

def saveFile(uploaded):
    with open(os.path.join(os.getcwd(),uploaded.name),"w") as f:
        strIo= StringIO(uploaded.getvalue().decode("utf-8"))
        f.write(strIo.read())
        return os.path.join(os.getcwd(),uploaded.name)

def main():
    st.write("# Keboola upload button")
    st.write("## A Streamlit Custom component")
    with st.expander("Keboola Tables"):
        tables=kb.keboola_table_list(
                keboola_URL="https://connection.north-europe.azure.keboola.com",
                keboola_key='<key>',
                # Button Label
                label="GET TABLES",
                # Key is mandatory and has to be unique
                key="zero",
                # if api_only= True than the button is not shown and the api call is fired directly
                api_only=False
        )
        st.selectbox("Tables",options= list(map(lambda v: v['id'], tables)))
    with st.expander("Keboola Buckets"):    
        buckets=kb.keboola_bucket_list(
                keboola_URL="https://connection.north-europe.azure.keboola.com",
                keboola_key='<key>',
                # Button Label
                label="GET BUCKETS",
                # Key is mandatory and has to be unique
                key="one",
                # if api_only= True than the button is not shown and the api call is fired directly
                api_only=False
        )
        st.selectbox("Buckets",options= list(map(lambda v: v['id'], buckets)))
    url = "http://www.dickimaw-books.com/latex/admin/html/examples/booklist.csv"
    st.write("Get a sample CSV here [link](%s)" % url)    
    fl=st.file_uploader("Drop a csv...",type="csv")    
    if hasattr(fl,'name'):
        # Streamlit uploader doesn't save the file to disk, only in mem. 
        # We need to save the file to disk to send it to Keboola python client
        fpath=saveFile(fl)
        with st.expander("Keboola Upload files"):    
            value = kb.keboola_upload(
                keboola_URL="https://connection.north-europe.azure.keboola.com",
                keboola_key='<key>',
                keboola_table_name="test-anthony",
                keboola_bucket_id='in.c-streamlit_output',
                keboola_file_path=fpath,
                keboola_primary_key=['id'],
                # Button Label
                label="UPLOAD FILE",
                # Key is mandatory and has to be unique
                key="two",
                # if api_only= True than the button is not shown and the api call is fired directly
                api_only=False
            )
            value