import streamlit as st
import pandas as pd
import numpy as np

st.title('My Data Analysis App')

st.markdown('## Upload a dataset and analyze it!')

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write(df.describe())

