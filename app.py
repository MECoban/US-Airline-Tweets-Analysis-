import pandas as pd
import numpy as np
import re
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

st.title('US Airline Tweets Analysis App')
st.sidebar.title('Sidebar Options')


# Function to extract state abbreviation from tweet_location
def extract_state(location):
    states = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", 
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", 
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", 
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", 
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", 
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", 
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", 
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", 
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", 
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }
    for abbr, name in states.items():
        pattern = r'\b' + re.escape(abbr) + r'\b|\b' + re.escape(name) + r'\b'
        if re.search(pattern, location, re.IGNORECASE):
            return abbr  # Return the state abbreviation for uniformity
    return None  # Return None if no state info is found

@st.cache_resource()
def load_data():
    data = pd.read_csv('data/clean_tweets.csv')
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    geo_data = pd.read_csv('data/US_GeoCode.csv')
    geo_data.rename(columns={'state': 'state_territory'}, inplace=True)
    data['state_abbreviation'] = data['tweet_location'].apply(lambda x: extract_state(str(x)))
    merged_data = pd.merge(data, geo_data, left_on='state_abbreviation', right_on='state_territory', how='left')
    return merged_data

data = load_data()

st.sidebar.subheader('Show Random Tweet')
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.markdown(f'### Random {random_tweet} Tweet:')
st.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown('### Number of tweets by sentiment')
sentiment_vis = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='sentiment_vis')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown('### Number of tweets by sentiment')
    if sentiment_vis == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color = "Tweets", height=500)
        st.plotly_chart(fig)
    elif sentiment_vis == 'Pie chart':
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

state_tweet_counts = data['state_abbreviation'].value_counts().reset_index()
state_tweet_counts.columns = ['state', 'tweets']
if not st.sidebar.checkbox('Hide tweet counts on map'):
    st.markdown('### Number of tweets by state')
    fig = px.choropleth(
        state_tweet_counts,
        locations='state',
        locationmode='USA-states',
        color='tweets',
        color_continuous_scale='Viridis',
        scope='usa',
        labels={'tweets':'Number of Tweets'}
    )
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.subheader('When and Where are users tweeting from?')
hour = st.sidebar.slider('Hour of day', 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close map', True):
    st.markdown('### Tweets locations based on the time of day')
    st.markdown(f'{len(modified_data)} tweets between {hour}:00 and {hour+1}:00')
    st.map(modified_data.dropna(subset=['latitude', 'longitude']))


st.sidebar.subheader('Breakdown airline tweets by sentiment')
st.markdown('### Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'))
airline_vis = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='airline_vis')

if airline_vis == 'Histogram':
    if len(choice) > 0:
        choice_data = data[data.airline.isin(choice)]
        fig_choice = px.histogram(choice_data, x='airline', color='airline_sentiment',
                                  category_orders={"airline_sentiment": ["negative", "neutral", "positive"]},
                                  labels={'airline_sentiment': 'Sentiment'}, height=600, width=800)

        st.plotly_chart(fig_choice)
elif airline_vis == 'Pie chart':
    if len(choice) > 0:
        choice_data = data[data.airline.isin(choice)]
        fig_choice = px.pie(choice_data, values='airline_sentiment', names='airline', title='Airline sentiment distribution')
        st.plotly_chart(fig_choice)

st.sidebar.header('Word Cloud')
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'), key='word_sentiment')

if not st.sidebar.checkbox('Close the Word Cloud', True, key='close_word_cloud'):
    st.subheader(f'Word cloud for {word_sentiment} sentiment')
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Hide the axes
    st.pyplot(fig)  # Display the figure with Streamlit
