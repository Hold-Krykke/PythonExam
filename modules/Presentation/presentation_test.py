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

    def Average(lst):
        myFloat = sum(lst) / len(lst)
        # print(myFloat)
        return myFloat


    average = {"Trump": {}, "Biden": {}}

    for date in trumptweets.keys():
        average["Trump"][date] = Average(trumptweets[date])
    for date in bidentweets.keys():
        average["Biden"][date] = Average(bidentweets[date])

    print(average)

    df = pd.DataFrame(average)
    print(df)

    return df


object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

df = makeDataframe(object_test_data)


def lineGraph(data):
    data.plot(kind="line")
    plt.show()


lineGraph(df)
