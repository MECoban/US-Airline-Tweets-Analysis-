import pandas as pd

file_path = "data/Tweets.csv"
tweets_data = pd.read_csv(file_path)

tweets_data.info(), tweets_data.head()

from datetime import datetime


columns_to_drop = ["airline_sentiment_gold", "negativereason_gold", "tweet_coord"]
tweets_cleaned = tweets_data.drop(columns=columns_to_drop)


tweets_cleaned["tweet_created"] = pd.to_datetime(
    tweets_cleaned["tweet_created"].str[:-6]
)


tweets_cleaned["negativereason"] = tweets_cleaned["negativereason"].fillna("None")
tweets_cleaned["negativereason_confidence"] = tweets_cleaned[
    "negativereason_confidence"
].fillna(0)


tweets_cleaned["text"] = tweets_cleaned["text"].str.replace(
    r"http\S+", "", regex=True
)  # Remove URLs
tweets_cleaned["text"] = tweets_cleaned["text"].str.replace(
    r"@\S+", "", regex=True
)  # Remove mentions
tweets_cleaned["text"] = tweets_cleaned["text"].str.replace(
    r"[^A-Za-z0-9\s]", "", regex=True
)  # Remove special characters
tweets_cleaned["text"] = tweets_cleaned[
    "text"
].str.lower()  # Convert text to lower case


tweets_cleaned.info(), tweets_cleaned.head()


cleaned_file_path = "data/clean_tweets.csv"
tweets_cleaned.to_csv(cleaned_file_path, index=False)
