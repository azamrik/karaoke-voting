from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import streamlit as st

def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg",
        username=st.secrets.get('db_credentials').get('username'),
        password=st.secrets.get('db_credentials').get('password'),
        host=st.secrets.get('db_credentials').get('url'),
        port=st.secrets.get('db_credentials').get('port'),
        database=st.secrets.get('db_credentials').get('database'),
    )
    return create_engine(url)
