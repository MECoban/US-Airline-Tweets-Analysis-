# US Airline Tweets Analysis App

## Overview
The US Airline Tweets Analysis App is a Streamlit-based interactive web application designed to analyze tweets about US airlines. It provides insights into sentiment distribution, tweet volume by state and time, and reasons for negative sentiments among tweets collected. This app aims to help users understand public perception and sentiment trends related to different airlines through visual and textual analysis.

## Dataset
The data used in this project comes from a CSV file named Tweets.csv, which is available on Kaggle. This dataset includes a variety of features related to tweets about US airlines, such as sentiment, reason for negative sentiment, tweet text, and metadata.

## Installation
To run this application, you will need Python installed on your system. Python 3.6 or higher is recommended. You can install the necessary libraries using the following command:


```
 pip install -r requirements.txt
```


## Project Structure

### clean.py: 

This script is used for data preprocessing. It cleans the data by removing unnecessary columns, handling missing values, and standardizing text fields.

### app.py: 
This is the main Streamlit application file that provides the web interface for interacting with the data.

### data/: 
This directory should contain the CSV files used by the application. Make sure to place the Tweets.csv and any other necessary data files here.

## Usage
To start the application, navigate to the directory containing app.py and run the following command:


```
streamlit run app.py
```

This will start the Streamlit server, and you should be able to access the application in your web browser at the address indicated by Streamlit.

## Features
Data Filtering: Users can filter tweets based on the time of day and specific airlines.
Sentiment Analysis: Visualization of sentiment distribution across tweets.
Geographical Insights: Display of tweets by state with an interactive map.
Detailed Sentiment Breakdown: Breakdown of tweets by airline and sentiment, with options for histogram and pie chart visualizations.
Word Clouds: Generation of word clouds to visualize the most frequent words within tweets of selected sentiments.
Random Tweet Display: Feature to display a random tweet based on the selected sentiment.

## Contributing
Contributions to the app are welcome. Please fork the repository and submit a pull request with your suggested changes.



