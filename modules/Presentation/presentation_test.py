# Presentation file
# Contains charts
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

# Getting the test_data.
test_data = get_data_from_csv(test_data_path)


def makeDataframeByDate(tweets):

    trumptweets = defaultdict(list)
    bidentweets = defaultdict(list)

    for tweet in tweets:
        ## IF THE TWEET IS ABOUT TRUMP OR BIDEN
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            bidentweets[tweet["date"]].append(
                tweet["sentiment_analysis"]["positive_procent"]
            )
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trumptweets[tweet["date"]].append(
                tweet["sentiment_analysis"]["positive_procent"]
            )

    def Average(lst):
        # GET AVERAGE OF A LIST
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


def positiveOrNegative(tweets):
    trumptweets = defaultdict(list)
    bidentweets = defaultdict(list)

    for tweet in tweets:
        ## IF THE TWEET IS ABOUT TRUMP OR BIDEN
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            bidentweets[tweet["date"]].append(tweet["sentiment_analysis"]["verdict"])
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trumptweets[tweet["date"]].append(tweet["sentiment_analysis"]["verdict"])

    print("TRUMP:")
    print(trumptweets)
    print()
    print("BIDEN")
    print(bidentweets)

    return None


def lineGraph(df):
    df.plot(kind="line")


def barPlot(df):
    df.groupby(["Trump", "Biden"])
    df.plot(kind="bar", rot=0, colors=["red", "blue"])


# TESTING
object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

df = positiveOrNegative(object_test_data)

# df = makeDataframeByDate(object_test_data)

# lineGraph(df)
# plt.show()
# barPlot(df)
# plt.show()
