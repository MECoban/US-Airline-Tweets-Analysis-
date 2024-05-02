import streamlit as st
import pandas as pd
import numpy as np

st.title('My Data Analysis App')
st.sidebar.title()
st.markdown('## Upload a dataset and analyze it!')
st.sidebar.markdown()

@st.cache(persist=True) # Cache decorator the data so it doesn't have to be loaded every time the app is run
def load_data():
    data = pd.read_csv('Tweets.csv')
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()
