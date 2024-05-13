import pandas as pd
import numpy as np
import re
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objects as go

st.title("US Airline Tweets Analysis App")
st.markdown(
    """
This app analyzes tweets about US airlines, providing insights into sentiment, tweet volume by state and time, and reasons for negative tweets.
"""
)

# Sidebar design
st.sidebar.title("Navigation and Filters")
st.sidebar.markdown("Use the sidebar to navigate different sections and apply filters.")


def extract_state(location):
    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
    }
    for abbr, name in states.items():
        pattern = r"\b" + re.escape(abbr) + r"\b|\b" + re.escape(name) + r"\b"
        if re.search(pattern, location, re.IGNORECASE):
            return abbr
    return None


@st.cache_resource()
def load_data():
    data = pd.read_csv("data/clean_tweets.csv")
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    geo_data = pd.read_csv("data/US_GeoCode.csv")
    geo_data.rename(columns={"state": "state_territory"}, inplace=True)
    data["state_abbreviation"] = data["tweet_location"].apply(
        lambda x: extract_state(str(x))
    )
    merged_data = pd.merge(
        data,
        geo_data,
        left_on="state_abbreviation",
        right_on="state_territory",
        how="left",
    )
    return merged_data


data = load_data()

# Hour range selector
st.sidebar.subheader("Filter Tweets by Hour")
hour_range = st.sidebar.slider("Hour of day", 0, 24, (3, 6), key="hour_range")
filtered_data = data[
    (data["tweet_created"].dt.hour >= hour_range[0])
    & (data["tweet_created"].dt.hour <= hour_range[1])
]
st.sidebar.markdown(
    f"Tweets from {hour_range[0]:02}:00 to {hour_range[1]:02}:00: **{len(filtered_data)}**"
)

# Visualization by sentiment
st.sidebar.subheader("Visualizations by Sentiment")
sentiment_vis = st.sidebar.selectbox(
    "Choose a chart type:", ["Histogram", "Pie chart"], key="sentiment_vis"
)
sentiment_count = filtered_data["airline_sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Tweets"]

if st.sidebar.checkbox("Display Sentiment Chart", True):
    st.subheader("Number of Tweets by Sentiment")
    st.markdown("This chart represents the distribution of tweet sentiments.")
    if sentiment_vis == "Histogram":
        fig = px.bar(
            sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500
        )
        st.plotly_chart(fig)
    elif sentiment_vis == "Pie chart":
        colors = {"negative": "darkred", "positive": "blue", "neutral": "white"}
        fig = px.pie(
            sentiment_count,
            values="Tweets",
            names="Sentiment",
            color="Sentiment",
            color_discrete_map=colors,
        )
        st.plotly_chart(fig)

# Tweets by state visualization
st.subheader("Tweets by State")
st.markdown(
    "This map shows the distribution of tweets across different states in the USA."
)
state_tweet_counts = filtered_data["state_abbreviation"].value_counts().reset_index()
state_tweet_counts.columns = ["state", "tweets"]
fig = px.choropleth(
    state_tweet_counts,
    locations="state",
    locationmode="USA-states",
    color="tweets",
    color_continuous_scale="Viridis",
    scope="usa",
    labels={"tweets": "Number of Tweets"},
)
st.plotly_chart(fig, use_container_width=True)


# Airline sentiment breakdown
st.sidebar.subheader("Breakdown by Airline and Sentiment")
airline_choice = st.multiselect(
    "Pick airlines",
    ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"),
    key="airline_choice",
)
airline_vis = st.radio(
    "Chart type:", ["Histogram", "Pie chart"], key="airline_vis_type"
)

if airline_choice:
    st.subheader("Breakdown of Airline Tweets by Sentiment")
    st.markdown(
        "This visualization shows the sentiment distribution for selected airlines."
    )
    choice_data = filtered_data[filtered_data.airline.isin(airline_choice)]
    if airline_vis == "Histogram":
        fig_choice = px.histogram(
            choice_data,
            x="airline",
            color="airline_sentiment",
            category_orders={"airline_sentiment": ["negative", "neutral", "positive"]},
            labels={"airline_sentiment": "Sentiment"},
            height=600,
            width=800,
        )
        st.plotly_chart(fig_choice)
    elif airline_vis == "Pie chart":
        fig_choice = px.pie(
            choice_data,
            values="airline_sentiment",
            names="airline",
            title="Airline Sentiment Distribution",
        )
        st.plotly_chart(fig_choice)

# Negative tweet reasons
st.sidebar.header("Detailed Analysis of Negative Tweets")
if st.sidebar.checkbox("Show Reasons for Negative Tweets", True):
    st.header("Analysis of Negative Tweets Reasons")
    st.markdown(
        "This section provides a deeper insight into the reasons behind negative tweets."
    )
    negative_tweets = filtered_data[filtered_data["airline_sentiment"] == "negative"]
    neg_reason_counts = negative_tweets["negativereason"].value_counts().reset_index()
    neg_reason_counts.columns = ["Reason", "Count"]
    select_chart_type = st.radio(
        "Chart type:", ["Bar chart", "Pie chart"], key="chart_type_neg"
    )

    if select_chart_type == "Bar chart":
        fig = px.bar(
            neg_reason_counts,
            x="Reason",
            y="Count",
            title="Reasons for Negative Tweets",
        )
        st.plotly_chart(fig)
    elif select_chart_type == "Pie chart":
        fig = px.pie(
            neg_reason_counts,
            values="Count",
            names="Reason",
            title="Reasons for Negative Tweets",
        )
        st.plotly_chart(fig)

# Random tweet display
st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
if st.sidebar.button("Show Random Tweet"):
    random_tweet_data = filtered_data.query("airline_sentiment == @random_tweet")
    if not random_tweet_data.empty:
        st.markdown(f"### Random {random_tweet} Tweet:")
        st.markdown(random_tweet_data[["text"]].sample(n=1).iat[0, 0])
    else:
        st.markdown("No tweets available for this selection.")

# Word Cloud
st.sidebar.header("Word Cloud for Sentiments")
if st.sidebar.checkbox("Display Word Cloud", True):
    word_sentiment = st.sidebar.radio(
        "Choose sentiment:", ("positive", "neutral", "negative"), key="word_sentiment"
    )
    st.subheader(f"Word cloud for {word_sentiment} sentiment")
    st.markdown(
        "The word cloud visualizes the most frequent words found in tweets for the selected sentiment."
    )
    df = filtered_data[filtered_data["airline_sentiment"] == word_sentiment]
    words = " ".join(df["text"])
    processed_words = " ".join(
        [
            word
            for word in words.split()
            if "http" not in word and not word.startswith("@") and word != "RT"
        ]
    )
    wordcloud = WordCloud(
        stopwords=STOPWORDS, background_color="white", width=800, height=640
    ).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
