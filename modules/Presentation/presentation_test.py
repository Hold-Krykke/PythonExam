# Presentation file
# Contains charts
# Start-point is this tutorial: https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk
from presentation_helpers import *
from test_data_generator import make_test_data
from collections import defaultdict

# Test Data Path
test_data_path = "../../data/test_tweets/presentation_test_tweets.csv"

"""
Example of data structure for the real data:
[
    {
        "tweet": "This tweet year",
        "hashtags": [
            "#MyFirstTweet"
        ],
        "people": [
            "@folketinget"
        ],
        "urls": [
            "runivn.dk"
        ],
        "author": "Runi Vedel",
        "date": "01/05/2020",
        "sentiment": {
            "result": Neutral / Positive / Negative, 
            "accuracy": 90
        }
    }, 
]
"""


# Getting the test_data.
test_data = get_data_from_csv(test_data_path)
# Manually testing if we got it how we want it.
# print(test_data.head())


def number_of_tweets_test(dataframe):
    # https://matplotlib.org/tutorials/introductory/customizing.html#matplotlib-rcparams
    plot_settings()
    array_of_airline_names = dataframe.airline
    # .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    unique_counts_of_airline = array_of_airline_names.value_counts()
    pie_plot = unique_counts_of_airline.plot(kind="pie", autopct="%1.0f%%")
    plt.show()


# number_of_tweets_test(test_data)


def sentiment_tweets_test(dataframe):
    plot_settings()
    dataframe.airline_sentiment.value_counts().plot(
        kind="pie", autopct="%1.0f%%", colors=["red", "yellow", "green"]
    )
    plt.show()


# sentiment_tweets_test(test_data)


def bar_plot_test(dataframe):
    # plot_settings()
    airline_sentiment = (
        dataframe.groupby(["airline", "airline_sentiment"])
        .airline_sentiment.count()
        .unstack()
    )
    airline_sentiment.plot(kind="bar")
    # save_plot(plt.gcf(), "test")
    plt.show()


# bar_plot_test(dataframe=test_data)


def makeDataframe(tweets):

    trumptweets = defaultdict(list)
    bidentweets = defaultdict(list)

    for tweet in tweets:
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            bidentweets[tweet["date"]].append(tweet["sentiment"]["result"])
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trumptweets[tweet["date"]].append(tweet["sentiment"]["result"])

    print("TRUMP TWEETS:")
    print(trumptweets)
    print()
    print()
    print("BIDEN TWEETS:")
    print(bidentweets)


def Average(lst):
    return sum(lst) / len(lst)


# date { Trump: [sentiment results], Biden}


# print(make_test_data(), "\n\n", make_test_data())
# print(object_test_data)
object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

makeDataframe(object_test_data)
