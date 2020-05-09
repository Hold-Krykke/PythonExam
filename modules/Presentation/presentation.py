# Presentation file
# Contains charts
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk
from helpers import *
from test_data_generator import make_test_data
from collections import defaultdict
import datetime


"""
How to use:

You have to have an array of tweets.
1. Sort
2. Get sentiment
3. Plot

First, you sort the tweets, using for example get_by_key_value or get_tweets_in_daterange
Then you use get_sentiment 
Then you feed the result of get_sentiment to a plotter function

"""

# FILTERING / SORTING FUNCTIONS START
def get_tweets_in_daterange(tweets, start_date, end_date):
    """
    Category: Sorter function

    Returns all tweets with "date" between start_date and end_date

    Parameters:

        tweets: array of tweets
        start_date and end_date are datetime objects

    Returns:

        Filtered list of tweets within start_date and end_date
    """
    if start_date > end_date:
        raise Exception("Start_date was before end_date.")

    return list(
        filter(
            lambda tweet: tweet["date"] <= end_date and tweet["date"] >= start_date,
            tweets,
        )
    )


def get_by_key_value(tweets, key, value):
    """
    Category: Sorter function

    Get tweets from tweet array, by key and value. 

    For example:
        
        key = hashtags
        value = #Biden

    Parameters:
        
        tweets = Array of tweets you want to filter
        key = String: one of: [hashtags, people, urls]
        value = String

    Returns: 

        Filtered List
    """

    # def custom_filter(tweet):
    #     # For use by .filter()
    #     if value in tweet[key]:
    #         return True
    #     else:
    #         return False

    # return list(filter(custom_filter, tweets))
    return list(filter(lambda tweet: value in tweet[key], tweets))


def get_by_sentiment(tweets, sentiment):
    """
    Not Yet Implemented
    Returns all tweets with a certain sentiment. 
    Positive, Negative or Uncertain 
    """

    return None


# FILTERING / SORTING FUNCTIONS DONE


def getSentiment(tweets):
    """
    Filter tweets using other methods, before you use this one. 
    """
    # Make a dict, where key is date and value is a list of all sentiments for that date
    tweets_dict = defaultdict(list)
    for tweet in tweets:
        tweets_dict[tweet["date"]].append(tweet["sentiment_analysis"]["verdict"])

    # Takes .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    for date in tweets_dict.keys():
        tweets_dict[date] = pd.Series(tweets_dict[date]).value_counts()

    # Makes a transposed dataframe sorted by index(date in this case)
    return pd.DataFrame(tweets_dict).T.sort_index()


# PLOTTING START


def pie_chart(df):
    """
    """
    plot = df.plot(kind="pie", autopct="%1.0f%%", title=f"Tweets.",)
    return plot


# PLOTTING END


# TESTING BELOW
# MAKE TEST DATA
object_test_data = []
for i in range(10000):
    object_test_data.append(make_test_data())

# Testing daterange
object_test_data = get_tweets_in_daterange(
    object_test_data, datetime.date(2020, 5, 19), datetime.date(2020, 5, 22)
)

# Testing getting tweets by hashtag
object_test_data = get_by_key_value(object_test_data, "hashtags", "#Trump")

plot_me = getSentiment(object_test_data)
# plot_me.plot(kind="bar", rot=0, title="Sentiment")
# print(plot_me)
# plot_me.plot(kind="line", title="Sentiment over time")
pie_chart(plot_me).show()
